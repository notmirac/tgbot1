from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "chat_messages.log"


def _append_line(line: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


async def log_chat_message(user_id: int, username: str | None, partner_name: str, partner_age: int, direction: str, text: str) -> None:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_text = (text or "").replace("\n", " ").strip()
    line = f"[{stamp}] user_id={user_id} username=@{username or '-'} partner={partner_name},{partner_age} direction={direction} text={clean_text}"
    await asyncio.to_thread(_append_line, line)


async def log_chat_event(user_id: int, username: str | None, event: str, details: str = "") -> None:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] user_id={user_id} username=@{username or '-'} event={event} details={details}"
    await asyncio.to_thread(_append_line, line)
