# parser.py

import time
import logging
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote
from curl_cffi.requests import AsyncSession

from config import CACHE_TTL_MINUTES

logger = logging.getLogger(__name__)

BASE_API_URL = "https://schedule.kantiana.ru/v1/api/lessons/group"

# Сервер (Railway) живёт по UTC, а студенты в Калининграде (UTC+2).
# Без этого «сегодня» между 00:00 и 02:00 по Калининграду было бы вчерашним днём.
TZ = ZoneInfo("Europe/Kaliningrad")

# Кэш в памяти: (группа, понедельник недели) -> (время сохранения, расписание)
_cache: dict[tuple[str, str], tuple[float, dict]] = {}


def today_date() -> date:
    """Сегодняшняя дата по Калининграду."""
    return datetime.now(TZ).date()


def week_monday(d: date) -> date:
    """Понедельник той недели, в которую попадает дата d."""
    return d - timedelta(days=d.weekday())


async def fetch_schedule(group: str, target: date | None = None) -> dict | None:
    """Загружает расписание группы на НЕДЕЛЮ, в которую попадает дата target
    (если target не указана, то на текущую неделю).
    Возвращает словарь {"YYYY-MM-DD": [пары]} или None при ошибке."""
    target = target or today_date()
    monday = week_monday(target)
    sunday = monday + timedelta(days=6)

    # 1. Смотрим в кэш
    key = (group, monday.isoformat())
    cached = _cache.get(key)
    if cached and time.monotonic() - cached[0] < CACHE_TTL_MINUTES * 60:
        return cached[1]

    date_from = monday.strftime("%Y-%m-%d")
    date_to = sunday.strftime("%Y-%m-%d")

    encoded_group = quote(group)
    url = f"{BASE_API_URL}?group={encoded_group}&date_from={date_from}&date_to={date_to}"
    logger.info(f"Целевой URL: {url}")

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://schedule.kantiana.ru/",
        "Origin": "https://schedule.kantiana.ru",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    try:
        # impersonate="chrome120" заставляет библиотеку копировать отпечатки Chrome
        async with AsyncSession(impersonate="chrome120") as session:

            # ШАГ 1: заходим на главную страницу, чтобы получить cookies
            logger.info("🍪 Заходим на главную страницу для получения cookies...")
            await session.get("https://schedule.kantiana.ru/", timeout=15)

            # ШАГ 2: запрос к API с теми же cookies и заголовками
            logger.info("📡 Отправляем запрос к API расписания...")
            response = await session.get(url, headers=headers, timeout=30)

            if response.status_code != 200:
                logger.error(f"❌ HTTP {response.status_code} для группы {group}")
                logger.error(f"Ответ сервера: {response.text[:500]}")
                return None

            # 👇 ВОТ ЗДЕСЬ БЫЛИ СЛОМАНЫ ОТСТУПЫ 👇
            data = response.json()

            logger.info(
                "API response: type=%s, keys=%s",
                type(data).__name__,
                list(data.keys()) if isinstance(data, dict) else "not a dict",
            )

            schedule = parse_lessons_data(data)

            # Пустой ответ не кэшируем: сначала нужно понять,
            # действительно ли API вернул пустое расписание.
            if not schedule:
                logger.warning(
                    "Парсер не извлёк ни одной пары для группы %r. "
                    "Фрагмент ответа API: %s",
                    group,
                    repr(data)[:2000],
                )
                return {}

            if len(_cache) > 500:
                _cache.clear()

            _cache[key] = (time.monotonic(), schedule)
            return schedule

    except Exception as e:
        logger.exception(f"❌ Критическая ошибка при запросе расписания: {e}")
        return None


def parse_lessons_data(data: dict | list) -> dict:
    schedule = {}
    lessons_list = data.get("items", data.get("data", data)) if isinstance(data, dict) else data

    if not isinstance(lessons_list, list):
        logger.warning(f"Неожиданный формат данных: {type(data)}")
        return schedule

    for lesson in lessons_list:
        date_str = lesson.get("date")
        if not date_str:
            continue

        date_key = str(date_str)[:10]

        # 1. Время: начало и конец (например, "10:10 - 11:40").
        #    "or ''" защищает от случая, когда сервер вернул null (None).
        start_time = lesson.get("start_time") or ""
        end_time = lesson.get("end_time") or ""
        if start_time and end_time:
            time_str = f"{start_time[:5]} - {end_time[:5]}"
        else:
            time_str = start_time[:5] if start_time else "—"

        # 2. Предмет: название + тип занятия
        discipline = lesson.get("discipline") or "Неизвестный предмет"
        load = lesson.get("load") or ""
        subject = f"{discipline} ({load})" if load else discipline

        # 3. Преподаватель: пытаемся собрать полное ФИО, иначе берем name или short
        teacher_obj = lesson.get("teacher") or {}
        if isinstance(teacher_obj, dict):
            full_name = f"{teacher_obj.get('last_name', '')} {teacher_obj.get('first_name', '')} {teacher_obj.get('patronymic', '')}".strip()
            teacher = full_name or teacher_obj.get('name') or teacher_obj.get('short') or "—"
        else:
            teacher = str(teacher_obj) if teacher_obj else "—"

        # 3.1 Номер пары (если API его отдает)
        lesson_num = lesson.get("lesson_number") or lesson.get("number") or lesson.get("pair") or ""

        # 4. Аудитория
        room = lesson.get("beautiful_room") or lesson.get("short_room") or lesson.get("room") or "—"
        if not room or str(room).lower() == "null":
            room = "Аудитория не указана"

        # 5. Подгруппа
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

    
    # Сортируем пары по времени в каждом дне
    for date_key in schedule:
        schedule[date_key].sort(key=lambda x: x["time"])

    return schedule


def get_today() -> str:
    return today_date().strftime("%Y-%m-%d")


def get_tomorrow() -> str:
    return (today_date() + timedelta(days=1)).strftime("%Y-%m-%d")


def get_week_dates(base_date: date | None = None) -> list[str]:
    d = base_date or today_date()
    monday = week_monday(d)
    return [(monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
