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

    # Максимально реалистичные заголовки
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
        # impersonate="chrome120" заставляет библиотеку притворяться настоящим Chrome 120
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

    if len(lessons_list) > 0:
        logger.info(f"API вернул ключи урока: {list(lessons_list[0].keys())}")

    for lesson in lessons_list:
        date_str = lesson.get("date") or lesson.get("lesson_date") or lesson.get("start_date")
        if not date_str:
            continue
            
        date_key = str(date_str)[:10]
        
        time_str = lesson.get("time") or lesson.get("start_time") or lesson.get("lesson_time") or lesson.get("beginTime") or "—"
        subject = lesson.get("subject") or lesson.get("discipline") or lesson.get("name") or lesson.get("discipline_name") or lesson.get("subject_name") or "Неизвестный предмет"
        teacher = lesson.get("teacher") or lesson.get("fio") or lesson.get("lecturer") or lesson.get("teacher_name") or lesson.get("employeeName") or "—"
        room = lesson.get("room") or lesson.get("audience") or lesson.get("cabinet") or lesson.get("room_name") or lesson.get("auditoryName") or "—"
        
        if date_key not in schedule:
            schedule[date_key] = []
            
        schedule[date_key].append({
            "time": time_str,
            "subject": subject,
            "teacher": teacher,
            "room": room
        })
        
    for date_key in schedule:
        schedule[date_key].sort(key=lambda x: str(x["time"]))
        
    return schedule

def get_today() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def get_tomorrow() -> str:
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

def get_week_dates() -> list[str]:
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    return [(monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
