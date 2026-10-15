import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import router
from database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

async def main():
    print("🚀 Запускаем бота в облаке...")
    
    await init_db()
    bot = Bot(token=BOT_TOKEN)

# 🔥 КЛЮЧЕВАЯ СТРОЧКА: удаляем webhook, если он был установлен ранее
    await bot.delete_webhook(drop_pending_updates=True)
    print("🧹 Webhook удалён (если был)")

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    print("🎉 БОТ РАБОТАЕТ!")

    await dp.start_polling(bot)

if __name__ == "__main__":
