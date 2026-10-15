import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import init_db
from handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

async def main():
    print("🚀 Запускаем бота...")
    
    # 1. Сначала создаём таблицы в базе данных!
    await init_db()
    
    bot = Bot(token=BOT_TOKEN)
    
    # 2. Гарантированно удаляем вебхук, чтобы не было конфликтов
    await bot.delete_webhook(drop_pending_updates=True)
    print("🧹 Webhook удалён")
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    
    print("🎉 БОТ РАБОТАЕТ И СЛУШАЕТ КОМАНДЫ!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
