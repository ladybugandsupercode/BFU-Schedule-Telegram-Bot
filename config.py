import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ВАЖНО: Путь к базе данных на постоянном диске Railway
DB_PATH = os.getenv("DB_PATH", "/app/data/bot.db")

SCHEDULE_BASE_URL = os.getenv("SCHEDULE_BASE_URL", "https://schedule.kantiana.ru")
CACHE_TTL_MINUTES = 30

# Официальный токен от IT-отдела БФУ
SCHEDULE_API_TOKEN = os.getenv("SCHEDULE_API_TOKEN", "")
