import asyncio
import logging
import random
from typing import Optional

from openai import AsyncOpenAI, OpenAIError

from config import config

logger = logging.getLogger(__name__)


def _make_client() -> AsyncOpenAI:
    kwargs: dict = {"api_key": config.openai_api_key}
    if config.openai_base_url:
        kwargs["base_url"] = config.openai_base_url
    return AsyncOpenAI(**kwargs)


_client: Optional[AsyncOpenAI] = None


def get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = _make_client()
    return _client


async def get_virtual_reply(user_message: str, partner_profile: dict, history: Optional[list[dict]] = None, lang: str = "ru") -> str:
    history = history or []
    partner_name = partner_profile.get("name", "Собеседник")
    partner_age = partner_profile.get("age", 22)
    partner_gender = partner_profile.get("gender", "ж")
    tone = "девушка" if partner_gender == "ж" else "мужчина"

    language_prompt = "Отвечай только на русском языке." if lang != "en" else "Reply only in English."
    system_prompt = (
        f"Ты ведешь переписку как обычный {tone} по имени {partner_name}, возраст {partner_age}. "
        f"{language_prompt} Пиши естественно, живо, короткими сообщениями, как в мессенджере. "
        "Не используй длинные абзацы. Иногда уместны эмодзи. Не говори, что ты AI, бот или программа. "
        "Не придумывай системные сообщения, говори только как собеседник."
    )

    messages: list[dict] = [{"role": "system", "content": system_prompt}]
    messages.extend(history[-20:])
    messages.append({"role": "user", "content": user_message})

    await asyncio.sleep(random.uniform(max(1.0, config.reply_delay_min), max(1.8, config.reply_delay_max - 1.0)))

    try:
        response = await get_client().chat.completions.create(
            model=config.chat_18_model or config.chat_model,
            messages=messages,
            max_tokens=220,
            temperature=0.9,
        )
        text = (response.choices[0].message.content or "").strip()
        return text or partner_profile.get("opener", "Привет 🙂")
    except OpenAIError as exc:
        logger.error("OpenAI API error: %s", exc)
        fallback = [
            "Привет 🙂 Расскажи что-нибудь о себе",
            "Как проходит вечер?",
            "Интересно с тобой, продолжай 😊",
            "А ты чем сейчас занят?",
        ]
        return random.choice(fallback)
    except Exception as exc:
        logger.exception("Unexpected error in get_virtual_reply: %s", exc)
        return partner_profile.get("opener", "Привет 🙂")


# обратная совместимость
async def get_ai_reply(user_message: str, mode: str = "chat", history: Optional[list[dict]] = None) -> str:
    profile = {"name": "Собеседник", "age": 23, "gender": "ж", "opener": "Привет 🙂"}
    return await get_virtual_reply(user_message=user_message, partner_profile=profile, history=history, lang="ru")
