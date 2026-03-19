# utils/profile_logger.py
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def log_profile(
    user_id: int,
    username: str | None,
    name: str,
    age: int,
    gender: str,
    action: str = "создана",
) -> None:
    """Логировать действие с анкетой."""
    uname = f"@{username}" if username else f"id:{user_id}"
    logger.info("Анкета %s: %s name=%s age=%d gender=%s", action, uname, name, age, gender)
