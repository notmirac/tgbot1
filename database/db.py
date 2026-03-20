
from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import AsyncIterator, Optional

import aiosqlite

logger = logging.getLogger(__name__)

DATA_DIR = Path(os.getenv("DATA_DIR", "/app/data"))
try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    pass

DB_PATH = DATA_DIR / "bot_database.db"


@asynccontextmanager
async def _db() -> AsyncIterator[aiosqlite.Connection]:
    db = await aiosqlite.connect(DB_PATH.as_posix(), timeout=30)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    try:
        yield db
    finally:
        await db.close()


async def _safe_add_column(db: aiosqlite.Connection, table: str, col: str, coltype: str) -> None:
    try:
        await db.execute(f"ALTER TABLE {table} ADD COLUMN {col} {coltype}")
        logger.info("Миграция: добавлена колонка %s.%s", table, col)
    except Exception:
        pass


async def _ensure_user_exists(
    db: aiosqlite.Connection,
    user_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    language_code: Optional[str] = None,
) -> None:
    await db.execute(
        """
        INSERT INTO users (user_id, username, first_name, language_code)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = COALESCE(excluded.username, users.username),
            first_name = COALESCE(excluded.first_name, users.first_name),
            language_code = COALESCE(excluded.language_code, users.language_code)
        """,
        (user_id, username, first_name, language_code),
    )


async def init_db() -> None:
    async with _db() as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                language_code TEXT,
                lang TEXT DEFAULT 'ru',
                preferred_gender TEXT,
                preferred_age_min INTEGER,
                preferred_age_max INTEGER,
                created_at TEXT DEFAULT (datetime('now'))
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                payment_id TEXT,
                amount INTEGER,
                currency TEXT,
                expires_at TEXT NOT NULL,
                issued_by INTEGER,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                profile_type TEXT NOT NULL DEFAULT 'normal',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS banned_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                username TEXT,
                banned_by INTEGER,
                reason TEXT,
                banned_at TEXT DEFAULT (datetime('now'))
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER,
                action TEXT,
                target_id INTEGER,
                target_name TEXT,
                details TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
            """
        )
        await db.commit()

        await _safe_add_column(db, "users", "lang", "TEXT DEFAULT 'ru'")
        await _safe_add_column(db, "users", "language_code", "TEXT")
        await _safe_add_column(db, "users", "preferred_gender", "TEXT")
        await _safe_add_column(db, "users", "preferred_age_min", "INTEGER")
        await _safe_add_column(db, "users", "preferred_age_max", "INTEGER")
        await _safe_add_column(db, "subscriptions", "issued_by", "INTEGER")
        await _safe_add_column(db, "banned_users", "username", "TEXT")
        await _safe_add_column(db, "banned_users", "banned_by", "INTEGER")
        await _safe_add_column(db, "banned_users", "reason", "TEXT")
        await _safe_add_column(db, "banned_users", "banned_at", "TEXT DEFAULT (datetime('now'))")
        await _safe_add_column(db, "admin_logs", "target_name", "TEXT")
        await db.commit()

    logger.info("БД готова: %s", DB_PATH)


async def add_or_update_user(user_id: int, username: Optional[str], first_name: Optional[str], language_code: Optional[str] = None) -> None:
    async with _db() as db:
        await _ensure_user_exists(db, user_id, username, first_name, language_code)
        await db.commit()


async def get_user_lang(user_id: int) -> str:
    async with _db() as db:
        row = await (await db.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))).fetchone()
    if row and row["lang"] in ("ru", "en"):
        return row["lang"]
    return "ru"


async def set_user_lang(user_id: int, lang: str) -> None:
    async with _db() as db:
        await db.execute(
            """
            INSERT INTO users (user_id, lang)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET lang = excluded.lang
            """,
            (user_id, lang),
        )
        await db.commit()


async def set_partner_preferences(user_id: int, preferred_gender: str, age_min: int, age_max: int) -> None:
    async with _db() as db:
        await _ensure_user_exists(db, user_id)
        await db.execute(
            """
            INSERT INTO users (user_id, preferred_gender, preferred_age_min, preferred_age_max)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                preferred_gender = excluded.preferred_gender,
                preferred_age_min = excluded.preferred_age_min,
                preferred_age_max = excluded.preferred_age_max
            """,
            (user_id, preferred_gender, age_min, age_max),
        )
        await db.commit()


async def get_partner_preferences(user_id: int) -> dict:
    async with _db() as db:
        row = await (
            await db.execute(
                "SELECT preferred_gender, preferred_age_min, preferred_age_max FROM users WHERE user_id = ?",
                (user_id,),
            )
        ).fetchone()
    if not row:
        return {"preferred_gender": "ж", "preferred_age_min": 18, "preferred_age_max": 25}
    return {
        "preferred_gender": row["preferred_gender"] or "ж",
        "preferred_age_min": row["preferred_age_min"] or 18,
        "preferred_age_max": row["preferred_age_max"] or 25,
    }


async def find_user_by_username(username: str) -> Optional[dict]:
    clean = username.strip().lstrip("@").lower()
    if not clean:
        return None
    async with _db() as db:
        row = await (
            await db.execute(
                "SELECT user_id, username, first_name FROM users WHERE LOWER(username) = ?",
                (clean,),
            )
        ).fetchone()
    return dict(row) if row else None


def format_user_label(user: dict) -> str:
    uname = f"@{user['username']}" if user.get("username") else f"id:{user['user_id']}"
    name = user.get("first_name") or ""
    return f"{uname} ({name})" if name else uname


async def get_stats() -> dict:
    async with _db() as db:
        now = datetime.utcnow().isoformat()

        total_users = (await (await db.execute("SELECT COUNT(*) AS c FROM users")).fetchone())[0]
        total_profiles = (await (await db.execute("SELECT COUNT(*) AS c FROM profiles")).fetchone())[0]
        total_banned = (await (await db.execute("SELECT COUNT(*) AS c FROM banned_users")).fetchone())[0]
        active_subs = (await (await db.execute("SELECT COUNT(DISTINCT user_id) FROM subscriptions WHERE expires_at > ?", (now,))).fetchone())[0]
        expired_subs = (await (await db.execute("SELECT COUNT(*) FROM subscriptions WHERE expires_at <= ?", (now,))).fetchone())[0]
        total_subs_issued = (await (await db.execute("SELECT COUNT(*) FROM subscriptions")).fetchone())[0]
        paid_subs = (await (await db.execute("SELECT COUNT(*) FROM subscriptions WHERE payment_id IS NOT NULL AND payment_id != 'manual_admin'")).fetchone())[0]
        manual_subs = (await (await db.execute("SELECT COUNT(*) FROM subscriptions WHERE payment_id = 'manual_admin'")).fetchone())[0]

        country_rows = await (await db.execute(
            "SELECT COALESCE(language_code, 'unknown') AS country, COUNT(*) AS cnt FROM users GROUP BY COALESCE(language_code, 'unknown') ORDER BY cnt DESC"
        )).fetchall()

    return {
        "total_users": total_users,
        "total_profiles": total_profiles,
        "total_banned": total_banned,
        "active_subs": active_subs,
        "expired_subs": expired_subs,
        "total_subs_issued": total_subs_issued,
        "paid_subs": paid_subs,
        "manual_subs": manual_subs,
        "countries": [(r["country"], r["cnt"]) for r in country_rows],
        # backward compatibility keys
        "active_subscriptions": active_subs,
        "total_subscriptions": total_subs_issued,
    }


async def add_subscription(user_id: int, payment_id: str, amount: int, currency: str, days: int, issued_by: Optional[int] = None) -> None:
    async with _db() as db:
        await _ensure_user_exists(db, user_id)
        last = await (
            await db.execute(
                "SELECT expires_at FROM subscriptions WHERE user_id = ? ORDER BY expires_at DESC LIMIT 1",
                (user_id,),
            )
        ).fetchone()
        now = datetime.utcnow()
        base = now
        if last and last["expires_at"]:
            try:
                old_expires = datetime.fromisoformat(last["expires_at"])
                if old_expires > now:
                    base = old_expires
            except Exception:
                pass
        new_expires = base + timedelta(days=days)
        await db.execute(
            "INSERT INTO subscriptions (user_id, payment_id, amount, currency, expires_at, issued_by) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, payment_id, amount, currency, new_expires.isoformat(), issued_by),
        )
        await db.commit()


async def revoke_subscription(user_id: int) -> None:
    async with _db() as db:
        await db.execute("UPDATE subscriptions SET expires_at = datetime('now', '-1 day') WHERE user_id = ?", (user_id,))
        await db.commit()


async def get_subscription_expires(user_id: int) -> Optional[datetime]:
    async with _db() as db:
        row = await (
            await db.execute(
                "SELECT expires_at FROM subscriptions WHERE user_id = ? ORDER BY expires_at DESC LIMIT 1",
                (user_id,),
            )
        ).fetchone()
    if not row or not row[0]:
        return None
    try:
        return datetime.fromisoformat(row[0])
    except Exception:
        return None


async def has_active_subscription(user_id: int) -> bool:
    expires = await get_subscription_expires(user_id)
    return expires is not None and expires > datetime.utcnow()


async def get_profile(user_id: int) -> Optional[dict]:
    async with _db() as db:
        row = await (
            await db.execute("SELECT user_id, name, age, gender, profile_type FROM profiles WHERE user_id = ?", (user_id,))
        ).fetchone()
    return dict(row) if row else None


async def save_profile(user_id: int, name: str, age: int, gender: str, profile_type: str = "normal") -> None:
    async with _db() as db:
        # Ключевой фикс: сначала гарантируем запись в users, чтобы не падал FOREIGN KEY.
        await _ensure_user_exists(db, user_id)
        await db.execute(
            """
            INSERT INTO profiles (user_id, name, age, gender, profile_type, updated_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                age = excluded.age,
                gender = excluded.gender,
                profile_type = excluded.profile_type,
                updated_at = datetime('now')
            """,
            (user_id, name, age, gender, profile_type),
        )
        await db.commit()


async def delete_profile(user_id: int) -> None:
    async with _db() as db:
        await db.execute("DELETE FROM profiles WHERE user_id = ?", (user_id,))
        await db.commit()


async def has_profile(user_id: int) -> bool:
    return await get_profile(user_id) is not None


async def is_banned(user_id: int) -> bool:
    async with _db() as db:
        row = await (await db.execute("SELECT 1 FROM banned_users WHERE user_id = ?", (user_id,))).fetchone()
    return row is not None


async def ban_user(user_id: int, banned_by: int, reason: str = "") -> None:
    async with _db() as db:
        row = await (await db.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))).fetchone()
        username = row[0] if row else None
        await db.execute(
            """
            INSERT INTO banned_users (user_id, username, banned_by, reason, banned_at)
            VALUES (?, ?, ?, ?, datetime('now'))
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                banned_by = excluded.banned_by,
                reason = excluded.reason,
                banned_at = datetime('now')
            """,
            (user_id, username, banned_by, reason),
        )
        await db.commit()


async def unban_user(user_id: int) -> None:
    async with _db() as db:
        await db.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
        await db.commit()


async def get_banned_list() -> list[dict]:
    async with _db() as db:
        rows = await (
            await db.execute("SELECT user_id, username, reason, banned_at FROM banned_users ORDER BY banned_at DESC")
        ).fetchall()
    return [dict(r) for r in rows]


async def add_admin_log(admin_id: int, action: str, target_id: int, target_name: str, details: str = "") -> None:
    async with _db() as db:
        await db.execute(
            "INSERT INTO admin_logs (admin_id, action, target_id, target_name, details) VALUES (?, ?, ?, ?, ?)",
            (admin_id, action, target_id, target_name, details),
        )
        await db.commit()


async def get_admin_logs(limit: int = 20) -> list[dict]:
    async with _db() as db:
        rows = await (
            await db.execute(
                "SELECT admin_id, action, target_id, target_name, details, created_at FROM admin_logs ORDER BY id DESC LIMIT ?",
                (limit,),
            )
        ).fetchall()
    return [dict(r) for r in rows]
