from .virtual_profiles import build_virtual_profile
from .ai_service import get_virtual_reply, get_ai_reply
from . import matchmaking

<<<<<<< HEAD
__all__ = ["build_virtual_profile", "get_virtual_reply", "get_ai_reply", "matchmaking"]
=======

async def get_ai_reply(message: str, mode: str = "chat", history=None):
    history = history or []
    partner = {"name": "AI", "age": 22, "gender": "ж"}
    return await get_virtual_reply(message, partner, history=history, lang="ru")


__all__ = ["build_virtual_profile", "get_virtual_reply", "get_ai_reply"]
>>>>>>> 4716f96 (add env and fixes)
