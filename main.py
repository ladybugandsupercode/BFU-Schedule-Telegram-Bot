import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def main():
    print("🚀 Запускаем минимального бота...")
    bot = Bot(token=BOT_TOKEN)
    
    # Сбрасываем вебхук, чтобы гарантированно работал polling
    await bot.delete_webhook(drop_pending_updates=True)
    
    dp = Dispatcher(storage=MemoryStorage())
    
    # САМАЯ ВАЖНАЯ СТРОКА: подключаем роутер из handlers.py
    dp.include_router(router)
    
    print("✅ Бот запущен и слушает команды!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
