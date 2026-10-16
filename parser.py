import logging
from datetime import datetime, timedelta
from urllib.parse import quote
from curl_cffi.requests import AsyncSession

logger = logging.getLogger(__name__)

BASE_API_URL = "https://schedule.kantiana.ru/v1/api/lessons/group"


async def fetch_schedule(group: str) -> dict | None:
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    
    date_from = monday.strftime("%Y-%m-%d")
    date_to = sunday.strftime("%Y-%m-%d")
    
    encoded_group = quote(group)
    url = f"{BASE_API_URL}?group={encoded_group}&date_from={date_from}&date_to={date_to}"
    logger.info(f"Fetching schedule: {url}")

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
        async with AsyncSession(impersonate="chrome120") as session:
            logger.info("Отправляем запрос через curl_cffi (Chrome 120 mode)...")
            response = await session.get(url, headers=headers, timeout=30)
            
            if response.status_code != 200:
                logger.error(f"❌ HTTP {response.status_code} for group {group}")
                logger.error(f"Ответ сервера: {response.text[:300]}")
                return None
            
            data = response.json()
            return parse_lessons_data(data)
            
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
        
        # 1. Время: объединяем начало и конец (например, "10:10 - 11:40")
        start_time = lesson.get("start_time", "")
        end_time = lesson.get("end_time", "")
        if start_time and end_time:
            time_str = f"{start_time[:5]} - {end_time[:5]}"
        else:
            time_str = start_time[:5] if start_time else "—"
        
        # 2. Предмет: название + тип занятия
        discipline = lesson.get("discipline", "Неизвестный предмет")
        load = lesson.get("load", "")
        subject = f"{discipline} ({load})" if load else discipline
        
        # 3. Преподаватель: берем краткое имя (short), если есть
        teacher_obj = lesson.get("teacher", {})
        if isinstance(teacher_obj, dict):
            teacher = teacher_obj.get("short") or teacher_obj.get("name", "—")
        else:
            teacher = str(teacher_obj) if teacher_obj else "—"
            
        # 4. Аудитория: приоритет у beautiful_room или short_room
        room = lesson.get("beautiful_room") or lesson.get("short_room") or lesson.get("room", "—")
        if not room or room == "null" or room == "":
            room = "Аудитория не указана"
            
        # 5. Подгруппа (очень полезно для студентов!)
        subgroup = lesson.get("subgroup", "")
        subgroup_text = f" | {subgroup}" if subgroup and subgroup != "Общая" else ""
        
        if date_key not in schedule:
            schedule[date_key] = []
            
        schedule[date_key].append({
            "time": time_str,
            "subject": subject + subgroup_text,
            "teacher": teacher,
            "room": room
        })
        
    # Сортируем пары по времени в каждом дне
    for date_key in schedule:
        schedule[date_key].sort(key=lambda x: x["time"])
        
    return schedule


def get_today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def get_tomorrow() -> str:
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


def get_week_dates() -> list[str]:
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    return [(monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
