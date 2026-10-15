import aiohttp
import logging
from datetime import datetime, timedelta
from urllib.parse import quote

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

    try:
        # МАКСИМАЛЬНО РЕАЛИСТИЧНЫЕ ЗАГОЛОВКИ НАСТОЯЩЕГО БРАУЗЕРА
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://schedule.kantiana.ru/",
            "Origin": "https://schedule.kantiana.ru",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=15) as resp:
                if resp.status == 403:
                    logger.error("❌ Доступ запрещен (403). Сайт БФУ блокирует запрос.")
                    # Попробуем прочитать, что именно отвечает сервер (часто там страница Cloudflare)
                    text = await resp.text()
                    logger.error(f"Ответ сервера при 403: {text[:300]}")
                    return None
                elif resp.status != 200:
                    logger.error(f"❌ HTTP {resp.status} for group {group}")
                    return None
                
                data = await resp.json()
                return parse_lessons_data(data)
                
    except Exception as e:
        logger.exception(f"❌ Error fetching schedule: {e}")
        return None

def parse_lessons_data(data: dict | list) -> dict:
    schedule = {}
    # API может вернуть список напрямую или словарь с ключом "items" или "data"
    lessons_list = data.get("items", data.get("data", data)) if isinstance(data, dict) else data
    
    if not isinstance(lessons_list, list):
        logger.warning(f"Unexpected data format: {type(data)}")
        return schedule

    if len(lessons_list) > 0:
        logger.info(f"API returned lesson keys: {list(lessons_list[0].keys())}")

    for lesson in lessons_list:
        # Пытаемся угадать название поля с датой
        date_str = lesson.get("date") or lesson.get("lesson_date") or lesson.get("start_date")
        if not date_str:
            continue
            
        date_key = str(date_str)[:10]  # Берём только "YYYY-MM-DD"
        
        # Пытаемся угадать названия остальных полей (адаптировано под возможные варианты БФУ)
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
        
    # Сортируем пары по времени в каждом дне
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
