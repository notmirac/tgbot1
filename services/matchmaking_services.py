# services/matchmaking.py
# ────────────────────────────────────────────────────────────
#  Система подбора собеседников.
#  Два типа очередей: обычная и 18+.
#  Хранит активные пары пользователей.
# ────────────────────────────────────────────────────────────

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ── Очереди ожидания ──────────────────────────────────────────────────────────
# Хранят user_id пользователей в поиске
_queue_normal: list[int] = []   # очередь обычного чата
_queue_adult:  list[int] = []   # очередь чата 18+

# ── Активные пары ─────────────────────────────────────────────────────────────
# { user_id: partner_id } — двустороннее хранение
_active_pairs: dict[int, int] = {}


# ── Очередь: добавить ─────────────────────────────────────────────────────────

def add_to_queue(user_id: int, mode: str = "normal") -> None:
    """Добавить пользователя в очередь поиска."""
    queue = _queue_adult if mode == "adult" else _queue_normal
    if user_id not in queue:
        queue.append(user_id)
        logger.info("User %d added to %s queue", user_id, mode)


def remove_from_queue(user_id: int) -> None:
    """Убрать пользователя из обеих очередей."""
    if user_id in _queue_normal:
        _queue_normal.remove(user_id)
    if user_id in _queue_adult:
        _queue_adult.remove(user_id)


# ── Очередь: найти пару ───────────────────────────────────────────────────────

def find_partner(user_id: int, mode: str = "normal") -> Optional[int]:
    """
    Найти собеседника для пользователя.
    Возвращает user_id партнёра или None если никого нет.
    """
    queue = _queue_adult if mode == "adult" else _queue_normal

    for candidate in queue:
        if candidate != user_id:
            return candidate
    return None


# ── Активные пары ─────────────────────────────────────────────────────────────

def create_pair(user1: int, user2: int) -> None:
    """Создать пару — убрать из очереди и запомнить соединение."""
    remove_from_queue(user1)
    remove_from_queue(user2)
    _active_pairs[user1] = user2
    _active_pairs[user2] = user1
    logger.info("Pair created: %d <-> %d", user1, user2)


def get_partner(user_id: int) -> Optional[int]:
    """Получить ID текущего собеседника."""
    return _active_pairs.get(user_id)


def end_chat(user_id: int) -> Optional[int]:
    """
    Завершить чат.
    Возвращает ID бывшего партнёра (чтобы уведомить его).
    """
    partner_id = _active_pairs.pop(user_id, None)
    if partner_id:
        _active_pairs.pop(partner_id, None)
        logger.info("Chat ended: %d <-> %d", user_id, partner_id)
    return partner_id


def is_in_chat(user_id: int) -> bool:
    """Проверить, находится ли пользователь в активном чате."""
    return user_id in _active_pairs


def is_in_queue(user_id: int) -> bool:
    """Проверить, находится ли пользователь в очереди."""
    return user_id in _queue_normal or user_id in _queue_adult


def queue_size(mode: str = "normal") -> int:
    """Размер очереди."""
    return len(_queue_adult if mode == "adult" else _queue_normal)
