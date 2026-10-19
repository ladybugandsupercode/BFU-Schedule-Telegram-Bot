import aiosqlite
import logging
from config import DB_PATH

logger = logging.getLogger(__name__)

async def init_db():
    """Инициализирует базу данных и добавляет недостающие столбцы, если их нет."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            # 1. Создаём базовую таблицу, если её вообще нет
            await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                student_group TEXT,
                language TEXT DEFAULT 'ru',
                last_cached_schedule TEXT,
                cache_updated_at INTEGER DEFAULT 0
            )
            """)
            
            # 2. МИГРАЦИЯ: Пробуем добавить новый столбец для версий уведомлений.
            # Если он уже есть, возникнет OperationalError, который мы спокойно игнорируем.
            try:
                await db.execute("ALTER TABLE users ADD COLUMN notified_version TEXT DEFAULT NULL")
                logger.info("✅ Добавлен столбец notified_version")
            except aiosqlite.OperationalError:
                pass  # Столбец уже существует, всё отлично

            await db.commit()
            logger.info("✅ База данных успешно инициализирована и проверена")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации БД: {e}")
        raise

async def set_user_group(telegram_id: int, group: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, student_group) VALUES (?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET student_group=excluded.student_group
        """, (telegram_id, group))
        await db.commit()

async def get_all_user_ids() -> list[int]:
    """Получает список ВСЕХ telegram_id пользователей, кто когда-либо запускал бота."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Убрали условие WHERE, теперь берем абсолютно всех из таблицы
        async with db.execute("SELECT telegram_id FROM users") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def set_user_language(telegram_id: int, language: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, language) VALUES (?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET language=excluded.language
        """, (telegram_id, language))
        await db.commit()

async def get_user_language(telegram_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT language FROM users WHERE telegram_id=?", (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else "ru"

async def save_cached_schedule(telegram_id: int, schedule_json: str, timestamp: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (telegram_id, last_cached_schedule, cache_updated_at) VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET 
                last_cached_schedule=excluded.last_cached_schedule,
                cache_updated_at=excluded.cache_updated_at
        """, (telegram_id, schedule_json, timestamp))
        await db.commit()

async def get_cached_schedule(telegram_id: int) -> tuple[str | None, int | None]:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT last_cached_schedule, cache_updated_at FROM users WHERE telegram_id=?", (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            return (row[0], row[1]) if row else (None, None)

# === СИСТЕМА УВЕДОМЛЕНИЙ ===

async def get_all_user_ids() -> list[int]:
    """Получает список всех telegram_id пользователей (всех, кто когда-либо писал боту)."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT telegram_id FROM users") as cursor:
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

async def get_user_notified_version(telegram_id: int) -> str | None:
    """Получает версию, о которой пользователь уже уведомлен."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT notified_version FROM users WHERE telegram_id=?", 
            (telegram_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row and len(row) > 0 else None

async def set_user_notified_version(telegram_id: int, version: str):
    """Отмечает, что пользователь уведомлен о данной версии."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users SET notified_version=? WHERE telegram_id=?
        """, (version, telegram_id))
        await db.commit()
