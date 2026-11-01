import time
import json
import asyncio
import logging
from pathlib import Path
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote
from curl_cffi.requests import AsyncSession

from config import CACHE_TTL_MINUTES, SCHEDULE_API_TOKEN

logger = logging.getLogger(__name__)

BASE_API_URL = "https://schedule.kantiana.ru/v1/api/lessons/group"
TZ = ZoneInfo("Europe/Kaliningrad")

# In-memory кэш (быстрый, но живёт только пока бот запущен)
_cache: dict[tuple[str, str], tuple[float, dict]] = {}

# Persistent кэш на диске (переживает перезапуски)
PERSISTENT_CACHE_PATH = "/app/data/schedule_cache.json"
PERSISTENT_CACHE_MAX_AGE_HOURS = 24  # После этого данные считаются "устаревшими"
PERSISTENT_CACHE_MAX_ENTRIES = 1000  # Лимит записей, чтобы файл не разрастался


def today_date() -> date:
    return datetime.now(TZ).date()


def week_monday(d: date) -> date:
    return d - timedelta(days=d.weekday())


# === PERSISTENT CACHE ===

def _load_persistent_cache() -> dict:
    try:
        if Path(PERSISTENT_CACHE_PATH).exists():
            with open(PERSISTENT_CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Не удалось загрузить persistent кэш: {e}")
    return {}


def _save_persistent_cache(cache: dict):
    try:
        Path(PERSISTENT_CACHE_PATH).parent.mkdir(parents=True, exist_ok=True)
        with open(PERSISTENT_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False)
    except Exception as e:
        logger.warning(f"Не удалось сохранить persistent кэш: {e}")


def _persistent_cache_key(group: str, monday: date) -> str:
    return f"{group}_{monday.isoformat()}"


def _get_from_persistent_cache(group: str, monday: date) -> tuple[dict | None, bool]:
    """
    Возвращает (data, is_stale).
    is_stale=True если данные старше MAX_AGE часов.
    """
    cache = _load_persistent_cache()
    key = _persistent_cache_key(group, monday)
    entry = cache.get(key)
    if not entry:
        return None, False
    age_hours = (time.time() - entry["timestamp"]) / 3600
    if age_hours > PERSISTENT_CACHE_MAX_AGE_HOURS:
        return entry["data"], True  # устаревшие, но всё равно отдаём как fallback
    return entry["data"], False


def _save_to_persistent_cache(group: str, monday: date, data: dict):
    cache = _load_persistent_cache()
    key = _persistent_cache_key(group, monday)
    # Ограничиваем размер кэша
    if len(cache) > PERSISTENT_CACHE_MAX_ENTRIES:
        sorted_keys = sorted(cache.keys(), key=lambda k: cache[k]["timestamp"])
        for k in sorted_keys[:500]:
            del cache[k]
    cache[key] = {"timestamp": time.time(), "data": data}
    _save_persistent_cache(cache)


# === API ЗАПРОС ===

async def fetch_schedule(group: str, target: date | None = None) -> dict | None:
    """Загружает расписание с API. Возвращает dict или None при ошибке."""
    target = target or today_date()
    monday = week_monday(target)
    sunday = monday + timedelta(days=6)

    key = (group, monday.isoformat())
    cached = _cache.get(key)
    if cached and time.monotonic() - cached[0] < CACHE_TTL_MINUTES * 60:
        return cached[1]

    date_from = monday.strftime("%Y-%m-%d")
    date_to = sunday.strftime("%Y-%m-%d")
    encoded_group = quote(group)
    url = f"{BASE_API_URL}?group={encoded_group}&date_from={date_from}&date_to={date_to}"

    headers = {"Accept": "application/json"}
    if SCHEDULE_API_TOKEN:
        headers["X-Schedule-Token"] = SCHEDULE_API_TOKEN

    max_retries = 2
    for attempt in range(max_retries):
        try:
            async with AsyncSession(impersonate="chrome120") as session:
                if attempt == 0:
                    logger.info(f"📡 Запрос к API для группы {group}...")
                else:
                    logger.info(f"🔄 Повторная попытка для группы {group}...")

                response = await session.get(url, headers=headers, timeout=10)

                if response.status_code == 429:
                    logger.warning("⏳ Лимит запросов.")
                    await asyncio.sleep(5)
                    continue

                if response.status_code != 200:
                    logger.error(f"❌ HTTP {response.status_code} для группы {group}")
                    return None

                data = response.json()
                schedule = parse_lessons_data(data)

                if not schedule:
                    return {}

                if len(_cache) > 500:
                    _cache.clear()
                _cache[key] = (time.monotonic(), schedule)
                return schedule

        except Exception as e:
            if "timed out" in str(e).lower() and attempt < max_retries - 1:
                logger.warning(f"⏳ Сервер БФУ не ответил за 10 сек. Пробуем ещё раз...")
                await asyncio.sleep(1)
                continue
            else:
                logger.error(f"❌ Ошибка запроса для {group}: {e}")
                return None

    return None


async def fetch_schedule_smart(group: str, target: date | None = None) -> tuple[dict | None, bool]:
    """
    Умный запрос: сначала API, при неудаче — persistent кэш.
    Возвращает (data, is_stale).
    is_stale=True если данные получены из кэша (API недоступен).
    """
    # 1. Пробуем получить свежие данные с API
    data = await fetch_schedule(group, target)
    if data is not None:
        # Сохраняем в persistent кэш для будущих fallback'ов
        target = target or today_date()
        monday = week_monday(target)
        _save_to_persistent_cache(group, monday, data)
        return data, False

    # 2. API недоступен — пробуем persistent кэш
    target = target or today_date()
    monday = week_monday(target)
    cached_data, is_stale = _get_from_persistent_cache(group, monday)
    if cached_data is not None:
        logger.info(f"⚠️ API недоступен, используем кэш для группы {group} (stale={is_stale})")
        return cached_data, True

    # 3. Ничего нет
    return None, False


# === ПАРСИНГ ===

def parse_lessons_data(data: dict | list) -> dict:
    schedule = {}
    lessons_list = data.get("items", data.get("data", data)) if isinstance(data, dict) else data
    if not isinstance(lessons_list, list):
        return schedule

    for lesson in lessons_list:
        date_str = lesson.get("date")
        if not date_str:
            continue
        date_key = str(date_str)[:10]

        start_time = lesson.get("start_time") or ""
        end_time = lesson.get("end_time") or ""
        time_str = f"{start_time[:5]} - {end_time[:5]}" if start_time and end_time else (start_time[:5] if start_time else "—")

        discipline = lesson.get("discipline") or "Неизвестный предмет"
        load = lesson.get("load") or ""
        subject = f"{discipline} ({load})" if load else discipline

        teacher_obj = lesson.get("teacher") or {}
        if isinstance(teacher_obj, dict):
            full_name = f"{teacher_obj.get('last_name', '')} {teacher_obj.get('first_name', '')} {teacher_obj.get('patronymic', '')}".strip()
            teacher = full_name or teacher_obj.get('name') or teacher_obj.get('short') or "—"
        else:
            teacher = str(teacher_obj) if teacher_obj else "—"

        lesson_num = lesson.get("lesson_number") or lesson.get("number") or lesson.get("pair") or ""
        room = lesson.get("beautiful_room") or lesson.get("short_room") or lesson.get("room") or "—"
        if not room or str(room).lower() == "null":
            room = "Аудитория не указана"

        subgroup = lesson.get("subgroup") or ""
        subgroup_text = f" | {subgroup}" if subgroup and subgroup != "Общая" else ""

        if date_key not in schedule:
            schedule[date_key] = []
        schedule[date_key].append({
            "time": time_str,
            "lesson_num": lesson_num,
            "subject": subject + subgroup_text,
            "teacher": teacher,
            "room": room
        })

    for date_key in schedule:
        schedule[date_key].sort(key=lambda x: x["time"])
    return schedule


def get_week_dates(base_date: date | None = None) -> list[str]:
    d = base_date or today_date()
    monday = week_monday(d)
    return [(monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
