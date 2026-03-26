# middlewares/throttle.py
import time
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.filters import CommandObject
from aiogram.types import Message


class ThrottleMiddleware(BaseMiddleware):
    """
    Антиспам middleware.
    - Для команд (/start, /owner и т.д.) — rate 3 сек
      (защита от зацикливания накопленных апдейтов)
    - Для обычных сообщений — rate 0.3 сек
    """

    def __init__(self, rate: float = 0.3, command_rate: float = 3.0):
        self._rate         = rate
        self._command_rate = command_rate
        self._last: dict[int, float]         = {}
        self._last_cmd: dict[int, float]     = {}

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id if event.from_user else None
        if not user_id:
            return await handler(event, data)

        now         = time.monotonic()
        is_command  = bool(event.text and event.text.startswith("/"))

        if is_command:
            last = self._last_cmd.get(user_id, 0)
            if now - last < self._command_rate:
                # Молча игнорируем дублированные команды
                return
            self._last_cmd[user_id] = now
        else:
            last = self._last.get(user_id, 0)
            if now - last < self._rate:
                return
            self._last[user_id] = now

        return await handler(event, data)
