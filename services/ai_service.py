from __future__ import annotations
import random
from typing import Any
from config import config

def _heuristic_reply(user_text: str, partner: dict | None, history: list[dict[str, str]] | None, lang: str) -> str:
    text = (user_text or "").strip()
    low = text.lower()
    history = history or []
    prev_assistant = [m["content"] for m in history if m.get("role") == "assistant"]
    partner_name = (partner or {}).get("name", "Собеседник" if lang == "ru" else "Partner")

    if lang == "ru":
        if "как тебя зовут" in low or "тебя зовут" in low:
            return f"Меня зовут {partner_name} 🙂 А тебя?"
        if "сколько тебе лет" in low or ("сколько" in low and "лет" in low):
            age = (partner or {}).get("age", 24)
            return f"Мне {age}. А тебе?"
        elif "привет" in low or "hello" in low or "hi" in low:
            options = ["Привет 🙂 Как ты?", "Приветик. Как настроение?", "Хай 🙂 Что делаешь?"]
        elif "как дела" in low:
            options = ["У меня всё хорошо 🙂 А у тебя?", "Нормально, спасибо 🙂 Как ты?", "Хорошо. А как у тебя дела?"]
        else:
            options = ["Интересно 🙂 Расскажи чуть подробнее.", "Поняла тебя. И что дальше?", "Хм, звучит любопытно 🙂", "А тебе самому что нравится больше всего?", "Ясно 🙂 Продолжай, интересно."]
    else:
        if "your name" in low or "what is your name" in low:
            return f"My name is {partner_name} 🙂 And yours?"
        if "how old are you" in low or ("how" in low and "old" in low):
            age = (partner or {}).get("age", 24)
            return f"I am {age}. What about you?"
        elif "hello" in low or "hi" in low or "hey" in low:
            options = ["Hi 🙂 How are you?", "Hey 🙂 How's your mood?", "Hello 🙂 What are you doing?"]
        elif "how are you" in low:
            options = ["I'm good 🙂 And you?", "Doing well, thanks 🙂 How about you?", "Pretty good 🙂 What about you?"]
        else:
            options = ["Interesting 🙂 Tell me a bit more.", "I see. What happened next?", "Hmm, that sounds curious 🙂", "What do you like most about it?", "Got it 🙂 Keep going."]

    for reply in options:
        if reply not in prev_assistant:
            return reply
    return random.choice(options)

async def get_virtual_reply(user_text: str, partner: dict | None = None, history: list[dict[str, str]] | None = None, lang: str = "ru") -> str:
    if not config.openai_api_key:
        return _heuristic_reply(user_text, partner, history, lang)
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=config.openai_api_key, base_url=config.openai_base_url)
        messages: list[dict[str, Any]] = []
        for item in (history or [])[-12:]:
            role = item.get("role")
            content = item.get("content")
            if role in {"user", "assistant"} and content:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": user_text})
        response = await client.chat.completions.create(
            model=config.chat_18_model or config.chat_model,
            messages=messages,
            temperature=0.9,
            max_tokens=120,
        )
        text = (response.choices[0].message.content or "").strip()
        if text:
            return text
    except Exception:
        pass
    return _heuristic_reply(user_text, partner, history, lang)
