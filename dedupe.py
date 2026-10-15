import time
from aiogram import BaseMiddleware
from aiogram.types import Message

WINDOW = 2.0  # секунды

class DedupeMiddleware(BaseMiddleware):
    def __init__(self):
        self._seen = {}

    async def __call__(self, handler, event: Message, data):
        key = (event.chat.id,
               event.from_user.id if event.from_user else None,
               (event.text or "").strip())
        now = time.monotonic()
        self._seen = {k: t for k, t in self._seen.items() if now - t < WINDOW}
        if key in self._seen:
            return None  # дубль, пропускаем
        self._seen[key] = now
        return await handler(event, data)
