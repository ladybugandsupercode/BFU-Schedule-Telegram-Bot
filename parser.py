import aiohttp
import logging
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from config import SCHEDULE_BASE_URL

logger = logging.getLogger(__name__)


async def fetch_schedule(group: str) -> dict:
    url = f"{SCHEDULE_BASE_URL}/group/{group}"
    logger.info(f"Fetching schedule: {url}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=15) as resp:
                if resp.status != 200:
                    logger.error(f"HTTP {resp.status} for group {group}")
                    return None
                html = await resp.text()

        return parse_html(html)
    except Exception as e:
        logger.exception(f"Error fetching schedule: {e}")
        return None


def parse_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    schedule = {}

    day_blocks = soup.select(".schedule-day")
    for day in day_blocks:
        date_str = day.select_one(".date").get_text(strip=True)
        try:
            date_obj = datetime.strptime(date_str, "%d.%m.%Y")
            key = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            continue

        lessons = []
        for lesson in day.select(".lesson"):
            lessons.append({
                "time": lesson.select_one(".time").get_text(strip=True),
                "subject": lesson.select_one(".subject").get_text(strip=True),
                "teacher": lesson.select_one(".teacher").get_text(strip=True) or "—",
                "room": lesson.select_one(".room").get_text(strip=True) or "—",
            })
        schedule[key] = lessons

    return schedule


def get_today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def get_tomorrow() -> str:
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


def get_week_dates() -> list[str]:
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    return [(monday + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]