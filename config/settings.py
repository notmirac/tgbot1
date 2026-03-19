# config/settings.py
# ────────────────────────────────────────────────────────────
#  Централизованная конфигурация бота.
#  Все параметры берутся из переменных окружения (.env).
# ────────────────────────────────────────────────────────────

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Загружаем переменные из файла .env (если он есть)
load_dotenv()


@dataclass
class Config:
    # ── Telegram ──────────────────────────────────────────────
    bot_token: str = field(default_factory=lambda: _require("BOT_TOKEN"))

    # ── OpenAI / совместимый API ──────────────────────────────
    openai_api_key: str = field(default_factory=lambda: _require("OPENAI_API_KEY"))
    openai_base_url: str | None = field(
        default_factory=lambda: os.getenv("OPENAI_BASE_URL") or None
    )

    # Модели
    chat_model: str = field(
        default_factory=lambda: os.getenv("CHAT_MODEL", "llama-3.3-70b-versatile")
    )
    chat_18_model: str = field(
        default_factory=lambda: os.getenv("CHAT_18_MODEL", "llama-3.3-70b-versatile")
    )

    # ── Платежи ───────────────────────────────────────────────
    # Токен платёжного провайдера (от @BotFather → Payments)
    payment_provider_token: str = field(
        default_factory=lambda: os.getenv("PAYMENT_PROVIDER_TOKEN", "")
    )
    # Цена в копейках (29900 = 299 руб.) или центах (999 = $9.99)
    subscription_price: int = field(
        default_factory=lambda: int(os.getenv("SUBSCRIPTION_PRICE", "29900"))
    )
    # Валюта: RUB, USD, EUR
    currency: str = field(
        default_factory=lambda: os.getenv("CURRENCY", "RUB")
    )
    # Срок подписки в днях
    subscription_days: int = field(
        default_factory=lambda: int(os.getenv("SUBSCRIPTION_DAYS", "30"))
    )

    # ── Фотографии 18+ ────────────────────────────────────────
    # Список file_id или URL-адресов фотографий
    photo_18_ids: list[str] = field(
        default_factory=lambda: [
            p.strip()
            for p in os.getenv("PHOTO_18_IDS", "").split(",")
            if p.strip()
        ]
    )

    # ── Задержка ответа (секунды) ─────────────────────────────
    reply_delay_min: float = 3.0   # минимальная задержка
    reply_delay_max: float = 7.0   # максимальная задержка


def _require(key: str) -> str:
    """Получить обязательную переменную окружения или выбросить ошибку."""
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Переменная окружения '{key}' не задана. "
            f"Проверь файл .env или переменные окружения системы."
        )
    return value


# Единственный экземпляр конфигурации для всего приложения
config = Config()
