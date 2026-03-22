# middlewares/throttle.py
# rate=0.2 — не блокирует быстрые нажатия кнопок листания анкет
import time
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import Message


class ThrottleMiddleware(BaseMiddleware):
    """Антиспам — не более 5 сообщений в секунду на пользователя."""

    def __init__(self, rate: float = 0.2):
        self._rate = rate
        self._last: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id if event.from_user else None
        if user_id:
            now  = time.monotonic()
            last = self._last.get(user_id, 0)
            if now - last < self._rate:
                return
            self._last[user_id] = now
        return await handler(event, data)
