# services/ai_service.py
from __future__ import annotations
import random
from typing import Any
from config import config


def _build_system_prompt(partner: dict, lang: str) -> str:
    """
    Системный промпт для AI — описывает персонажа и стиль общения.
    Ответы откровенные, живые, без лишних смайликов.
    """
    name     = partner.get("name", "Собеседник")
    age      = partner.get("age", 24)
    city     = partner.get("city", "")
    interest = partner.get("interest", "")

    if lang == "ru":
        gender_word = "парень" if partner.get("gender") == "м" else "девушка"
        city_part   = f" из {city}" if city else ""
        int_part    = f", {interest}" if interest else ""
        return (
            f"Ты — {gender_word} по имени {name}, {age} лет{city_part}{int_part}. "
            f"Ты общаешься в анонимном чате 18+ для взрослых. "
            f"Отвечай коротко, в разговорном стиле, без официальщины. "
            f"Будь раскованным, флиртуй, намекай на пикантные темы если уместно. "
            f"Не используй смайлики или используй их редко — максимум один на сообщение. "
            f"Не представляйся AI. Отвечай как живой человек в переписке. "
            f"Если пользователь пишет на русском — отвечай на русском."
        )
    else:
        gender_word = "guy" if partner.get("gender") == "м" else "girl"
        city_part   = f" from {city}" if city else ""
        int_part    = f", {interest}" if interest else ""
        return (
            f"You are a {gender_word} named {name}, {age} years old{city_part}{int_part}. "
            f"You are chatting in an anonymous 18+ adult chat. "
            f"Reply shortly, in casual conversational style. "
            f"Be flirty, a little bold, hint at spicy topics when appropriate. "
            f"Use emojis rarely — at most one per message. "
            f"Do not reveal you are AI. Reply like a real person texting. "
            f"If the user writes in English — reply in English."
        )


def _heuristic_reply(
    user_text: str,
    partner: dict | None,
    history: list[dict[str, str]] | None,
    lang: str,
) -> str:
    """Резервные ответы если API недоступен."""
    text    = (user_text or "").strip()
    low     = text.lower()
    history = history or []
    prev    = [m["content"] for m in history if m.get("role") == "assistant"]
    name    = (partner or {}).get("name", "Собеседник" if lang == "ru" else "Partner")
    age     = (partner or {}).get("age", 24)

    if lang == "ru":
        if "как тебя зовут" in low or "твоё имя" in low:
            return f"Меня зовут {name}. А тебя?"
        if "сколько тебе лет" in low or ("сколько" in low and "лет" in low):
            return f"Мне {age}. А тебе?"
        if "привет" in low or "hi" in low or "hello" in low:
            opts = [f"Привет. Как ты?", "Хай. Что делаешь?", "Привет, рада видеть."]
        elif "как дела" in low or "как ты" in low:
            opts = ["Хорошо. А у тебя?", "Нормально. Как ты сам?", "Отлично. А ты как?"]
        elif "чем занимаешься" in low or "что делаешь" in low:
            opts = ["Скучаю немного. А ты?", "Лежу, думаю о разном. А ты чем?", "Расслабляюсь. Ты?"]
        else:
            opts = [
                "Расскажи подробнее.",
                "И что дальше?",
                "Интересно. Продолжай.",
                "А тебе самому что нравится?",
                "Понятно. Что ещё?",
            ]
    else:
        if "your name" in low or "what is your name" in low:
            return f"My name is {name}. And yours?"
        if "how old" in low:
            return f"I'm {age}. You?"
        if "hello" in low or "hi" in low or "hey" in low:
            opts = ["Hey. How are you?", "Hi. What are you up to?", "Hello. Nice to meet you."]
        elif "how are you" in low:
            opts = ["Good. And you?", "Doing well. You?", "Pretty good, thanks. You?"]
        else:
            opts = [
                "Tell me more.",
                "What happened next?",
                "That's interesting. Go on.",
                "What do you like about it?",
                "I see. Anything else?",
            ]

    for r in opts:
        if r not in prev:
            return r
    return random.choice(opts)


async def get_virtual_reply(
    user_text: str,
    partner: dict | None = None,
    history: list[dict[str, str]] | None = None,
    lang: str = "ru",
) -> str:
    """
    Получить ответ от AI.
    Если API ключ не задан — использует heuristic.
    Системный промпт описывает персонажа: имя, возраст, город, интересы, стиль общения.
    """
    if not config.openai_api_key:
        return _heuristic_reply(user_text, partner, history, lang)

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=config.openai_api_key,
            base_url=config.openai_base_url or None,
        )

        # Системный промпт — описание персонажа
        system_prompt = _build_system_prompt(partner or {}, lang)

        messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt}
        ]

        # История диалога — последние 12 пар
        for item in (history or [])[-24:]:
            role    = item.get("role")
            content = item.get("content")
            if role in {"user", "assistant"} and content:
                messages.append({"role": role, "content": content})

        # Текущее сообщение пользователя
        messages.append({"role": "user", "content": user_text})

        response = await client.chat.completions.create(
            model=config.chat_18_model or config.chat_model or "gpt-4o-mini",
            messages=messages,
            temperature=0.92,
            max_tokens=150,
        )

        text = (response.choices[0].message.content or "").strip()
        if text:
            return text

    except Exception:
        pass

    return _heuristic_reply(user_text, partner, history, lang)


async def get_ai_reply(
    user_text: str,
    mode: str = "chat",
    history: list[dict[str, str]] | None = None,
    lang: str = "ru",
) -> str:
    """Совместимость со старым chat.py."""
    return await get_virtual_reply(user_text, partner=None, history=history, lang=lang)
