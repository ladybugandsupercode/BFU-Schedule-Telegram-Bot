import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import init_db
from handlers import router

# Включаем ПОДРОБНОЕ логирование
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    print("🚀 Запускаем бота...")
    
    # Проверяем токен
    if not BOT_TOKEN:
        print("❌ ОШИБКА: Токен не найден в .env!")
        return
    
    print(f"✅ Токен найден: {BOT_TOKEN[:10]}...{BOT_TOKEN[-10:]}")
    
    try:
        print("📦 Инициализируем базу данных...")
        await init_db()
        print("✅ База данных готова")
        
        print("🤖 Создаём бота...")
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(router)
        
        print("✅ Бот создан, запускаем polling...")
        print("🎉 БОТ ЗАПУЩЕН И РАБОТАЕТ!")
        print("📱 Открой Telegram и напиши /start")
        
        await dp.start_polling(bot)
        
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        logger.exception("Детали ошибки:")


if __name__ == "__main__":
    asyncio.run(main())