import time
import asyncio
import logging
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote
from curl_cffi.requests import AsyncSession

from config import CACHE_TTL_MINUTES, SCHEDULE_API_TOKEN

logger = logging.getLogger(__name__)

BASE_API_URL = "https://schedule.kantiana.ru/v1/api/lessons/group"
TZ = ZoneInfo("Europe/Kaliningrad")
_cache: dict[tuple[str, str], tuple[float, dict]] = {}


def today_date() -> date:
    return datetime.now(TZ).date()

def week_monday(d: date) -> date:
    return d - timedelta(days=d.weekday())


async def fetch_schedule(group: str, target: date | None = None) -> dict | None:
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
    logger.info(f"Целевой URL: {url}")

    headers = {"Accept": "application/json"}
    if SCHEDULE_API_TOKEN:
        headers["X-Schedule-Token"] = SCHEDULE_API_TOKEN
        logger.info("🔑 Используем официальный токен БФУ")

    try:
        async with AsyncSession(impersonate="chrome120") as session:
            response = await session.get(url, headers=headers, timeout=30, verify=False)

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After", "60")
                logger.warning(f"⏳ Лимит запросов. Ждем {retry_after} сек.")
                await asyncio.sleep(int(retry_after))
                response = await session.get(url, headers=headers, timeout=30)

            if response.status_code != 200:
                logger.error(f"❌ HTTP {response.status_code} для группы {group}")
                return None

            data = response.json()
            schedule = parse_lessons_data(data)

            if not schedule:
                logger.warning(f"Пустое расписание для группы {group}")
                return {}

            if len(_cache) > 500:
                _cache.clear()
            _cache[key] = (time.monotonic(), schedule)
            return schedule

    except Exception as e:
        logger.exception(f"❌ Ошибка запроса: {e}")
        return None


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
