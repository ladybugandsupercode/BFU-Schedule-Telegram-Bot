import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = os.getenv("DB_PATH", "bot.db")
SCHEDULE_BASE_URL = os.getenv("SCHEDULE_BASE_URL", "https://schedule.kantiana.ru")
CACHE_TTL_MINUTES = 30