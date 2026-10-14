import aiosqlite
from config import DB_PATH
import logging

logger = logging.getLogger(__name__)


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                student_group TEXT,
                language TEXT DEFAULT 'ru',
                last_cached_schedule TEXT,
                cache_updated_at INTEGER DEFAULT 0
            )
        """)
        await db.commit()
    logger.info("Database initialized")


async def set_user_group(telegram_id: int, group: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, student_group) VALUES (?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET student_group=excluded.student_group
        """, (telegram_id, group))
        await db.commit()


async def get_user_group(telegram_id: int) -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT student_group FROM users WHERE telegram_id=?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def set_user_language(telegram_id: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, language) VALUES (?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET language=excluded.language
        """, (telegram_id, lang))
        await db.commit()


async def get_user_language(telegram_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT language FROM users WHERE telegram_id=?", (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row and row[0] else "ru"


async def get_cached_schedule(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT last_cached_schedule, cache_updated_at FROM users WHERE telegram_id=?",
            (telegram_id,)
        ) as cursor:
            return await cursor.fetchone()


async def save_cached_schedule(telegram_id: int, schedule_json: str, timestamp: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users SET last_cached_schedule=?, cache_updated_at=?
            WHERE telegram_id=?
        """, (schedule_json, timestamp, telegram_id))
        await db.commit()