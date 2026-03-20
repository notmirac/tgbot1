import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Переменная окружения '{key}' не задана. "
            f"Проверь файл .env или переменные окружения системы."
        )
    return value

@dataclass
class Config:
    bot_token: str = field(default_factory=lambda: _require("BOT_TOKEN"))
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    openai_base_url: str | None = field(default_factory=lambda: os.getenv("OPENAI_BASE_URL") or None)

    chat_model: str = field(default_factory=lambda: os.getenv("CHAT_MODEL", "llama-3.3-70b-versatile"))
    chat_18_model: str = field(default_factory=lambda: os.getenv("CHAT_18_MODEL", "llama-3.3-70b-versatile"))

    payment_provider_token: str = field(default_factory=lambda: os.getenv("PAYMENT_PROVIDER_TOKEN", ""))

    subscription_price_rub: int = field(default_factory=lambda: int(os.getenv("SUBSCRIPTION_PRICE_RUB", "30000")))
    subscription_price_usd: int = field(default_factory=lambda: int(os.getenv("SUBSCRIPTION_PRICE_USD", "300")))
    subscription_days: int = field(default_factory=lambda: int(os.getenv("SUBSCRIPTION_DAYS", "30")))

    # Совместимость со старыми файлами проекта
    currency: str = field(default_factory=lambda: os.getenv("CURRENCY", "RUB"))
    subscription_price: int = field(default_factory=lambda: int(os.getenv("SUBSCRIPTION_PRICE", "30000")))

    admin_id: int = field(default_factory=lambda: int(os.getenv("ADMIN_ID", "8592334405")))
    admin_username: str = field(default_factory=lambda: os.getenv("ADMIN_USERNAME", "@Alinka481"))

    photo_18_ids: list[str] = field(
        default_factory=lambda: [p.strip() for p in os.getenv("PHOTO_18_IDS", "").split(",") if p.strip()]
    )

    reply_delay_min: float = 2.0
    reply_delay_max: float = 5.0

config = Config()
