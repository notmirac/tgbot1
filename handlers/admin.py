
import logging
from datetime import datetime
from typing import Optional

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
)

from database import (
    add_subscription, get_subscription_expires,
    revoke_subscription, find_user_by_username,
    format_user_label, get_stats, get_profile,
    ban_user, unban_user, is_banned, get_banned_list,
)

logger = logging.getLogger(__name__)
router = Router()

OWNER_ID = 8592334405


def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID


class AdminStates(StatesGroup):
    waiting_give_username = State()
    waiting_give_days = State()
    waiting_revoke = State()
    waiting_check = State()
    waiting_ban_username = State()
    waiting_ban_reason = State()
    waiting_unban = State()


def admin_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="adm_stats")],
        [InlineKeyboardButton(text="💳 Подписки", callback_data="adm_subs")],
        [InlineKeyboardButton(text="🔒 Баны", callback_data="adm_bans")],
        [InlineKeyboardButton(text="🚫 Список банов", callback_data="adm_banlist")],
    ])


def subs_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Выдать подписку", callback_data="adm_give")],
        [InlineKeyboardButton(text="❌ Забрать подписку", callback_data="adm_revoke")],
        [InlineKeyboardButton(text="🔍 Проверить", callback_data="adm_check")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="adm_back")],
    ])


def bans_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚫 Забанить", callback_data="adm_ban")],
        [InlineKeyboardButton(text="✅ Разбанить", callback_data="adm_unban")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="adm_back")],
    ])


def back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="adm_back")],
    ])


def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="adm_cancel")],
    ])


async def resolve_user_safe(username_input: str) -> tuple[Optional[dict], str]:
    clean = (username_input or "").strip().lstrip("@")
    if not clean:
        return None, "⚠️ Введи @username пользователя."
    if clean.isdigit():
        return None, "⚠️ Вводи @username, а не цифровой ID.\nПример: @username"
    user = await find_user_by_username(clean)
    if not user:
        return None, (
            f"❌ Пользователь @{clean} не найден.\n\n"
            "Пользователь должен сначала написать боту /start"
        )
    return user, ""


async def _show_main_menu(target: Message | CallbackQuery) -> None:
    text = "⚙️ <b>Админ-панель</b>\n\n👑 Добро пожаловать, владелец!"
    kb = admin_main_kb()
    if isinstance(target, CallbackQuery):
        try:
            await target.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
        except Exception:
            await target.message.answer(text, reply_markup=kb, parse_mode="HTML")
        await target.answer()
    else:
        await target.answer(text, reply_markup=kb, parse_mode="HTML")


@router.message(Command("owner"))
@router.message(F.text.casefold() == "owner")
async def cmd_owner(message: Message, state: FSMContext) -> None:
    if not is_owner(message.from_user.id):
        return
    await state.clear()
    await _show_main_menu(message)


@router.callback_query(F.data == "adm_back")
async def adm_back(call: CallbackQuery, state: FSMContext) -> None:
    if not is_owner(call.from_user.id):
        await call.answer()
        return
    await state.clear()
    await _show_main_menu(call)


@router.callback_query(F.data == "adm_cancel")
async def adm_cancel(call: CallbackQuery, state: FSMContext) -> None:
    if not is_owner(call.from_user.id):
        await call.answer()
        return
    await state.clear()
    await _show_main_menu(call)


@router.callback_query(F.data == "adm_stats")
async def adm_stats(call: CallbackQuery) -> None:
    if not is_owner(call.from_user.id):
        await call.answer()
        return
    await call.answer()

    s = await get_stats()
    text = (
        "📊 <b>Статистика бота</b>\n\n"
        "👥 <b>Пользователи:</b>\n"
        f"  Всего: <b>{s.get('total_users', 0)}</b>\n"
        f"  Анкет: <b>{s.get('total_profiles', 0)}</b>\n"
        f"  Забанено: <b>{s.get('total_banned', 0)}</b>\n\n"
        "💳 <b>Подписки:</b>\n"
        f"  Активных: <b>{s.get('active_subscriptions', 0)}</b>\n"
        f"  Выдано всего: <b>{s.get('total_subscriptions', 0)}</b>\n"
    )
    await call.message.edit_text(text, reply_markup=back_kb(), parse_mode="HTML")


@router.callback_query(F.data == "adm_subs")
async def adm_subs(call: CallbackQuery) -> None:
    if not is_owner(call.from_user.id):
        await call.answer()
        return
    await call.answer()
    await call.message.edit_text(
        "💳 <b>Управление подписками</b>",
        reply_markup=subs_kb(), parse_mode="HTML",
    )


@router.callback_query(F.data == "adm_give")
async def adm_give_start(call: CallbackQuery, state: FSMContext) -> None:
    if not is_owner(call.from_user.id):
        await call.answer()
        return
    await call.answer()
    await state.set_state(AdminStates.waiting_give_username)
    await call.message.edit_text(
        "✅ <b>Выдать подписку</b>\n\n"
        "Введи @username пользователя:\n"
        "<i>Пример: @username или username</i>",
        reply_markup=cancel_kb(), parse_mode="HTML",
    )


@router.message(AdminStates.waiting_give_username)
async def adm_give_username(message: Message, state: FSMContext) -> None:
    if not is_owner(message.from_user.id):
        return
    user, error = await resolve_user_safe(message.text)
    if not user:
        await message.answer(error, reply_markup=cancel_kb(), parse_mode="HTML")
        return

    label = format_user_label(user)
    await state.update_data(target_id=user["user_id"], target_label=label)
    await state.set_state(AdminStates.waiting_give_days)
    await message.answer(
        f"👤 Найден: <b>{label}</b>\n\nНа сколько дней выдать подписку?\n<i>Введи число, например: 30</i>",
        reply_markup=cancel_kb(), parse_mode="HTML",
    )


@router.message(AdminStates.waiting_give_days)
async def adm_give_days(message: Message, state: FSMContext) -> None:
    if not is_owner(message.from_user.id):
        return
    try:
        days = int((message.text or "").strip())
        if days <= 0:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Введи число дней (например: 30):", reply_markup=cancel_kb())
        return

    data = await state.get_data()
    target_id = data["target_id"]
    target_label = data["target_label"]

    await add_subscription(
        user_id=target_id,
        payment_id="manual_admin",
        amount=0,
        currency="RUB",
        days=days,
        issued_by=message.from_user.id,
    )

    expires = await get_subscription_expires(target_id)
    expires_str = expires.strftime("%d.%m.%Y") if expires else "—"

    await state.clear()
    await message.answer(
        f"✅ <b>Подписка выдана!</b>\n"
        f"👤 {target_label}\n"
        f"📅 Действует до: <b>{expires_str}</b>",
        reply_markup=admin_main_kb(), parse_mode="HTML",
    )
    try:
        await message.bot.send_message(
            target_id,
            f"🎉 Тебе выдан доступ на <b>{days} дней</b>!\n📅 До: <b>{expires_str}</b>",
            parse_mode="HTML",
        )
    except Exception:
        pass


@router.callback_query(F.data == "adm_revoke")
async def adm_revoke_start(call: CallbackQuery, state: FSMContext) -> None:
    if not is_owner(call.from_user.id):
        await call.answer()
        return
    await call.answer()
    await state.set_state(AdminStates.waiting_revoke)
    await call.message.edit_text(
        "❌ <b>Забрать подписку</b>\n\nВведи @username:",
        reply_markup=cancel_kb(), parse_mode="HTML",
    )


@router.message(AdminStates.waiting_revoke)
async def adm_revoke_do(message: Message, state: FSMContext) -> None:
    if not is_owner(message.from_user.id):
        return
    user, error = await resolve_user_safe(message.text)
    if not user:
        await message.answer(error, reply_markup=cancel_kb(), parse_mode="HTML")
        return

    label = format_user_label(user)
    await revoke_subscription(user["user_id"])
    await state.clear()
    await message.answer(
        f"✅ Подписка у <b>{label}</b> отозвана.",
        reply_markup=admin_main_kb(), parse_mode="HTML",
    )
    try:
        await message.bot.send_message(user["user_id"], "❌ Твоя подписка была отозвана администратором.")
    except Exception:
        pass


@router.callback_query(F.data == "adm_check")
async def adm_check_start(call: CallbackQuery, state: FSMContext) -> None:
    if not is_owner(call.from_user.id):
        await call.answer()
        return
    await call.answer()
    await state.set_state(AdminStates.waiting_check)
    await call.message.edit_text(
        "🔍 <b>Проверить пользователя</b>\n\nВведи @username:",
        reply_markup=cancel_kb(), parse_mode="HTML",
    )


@router.message(AdminStates.waiting_check)
async def adm_check_do(message: Message, state: FSMContext) -> None:
    if not is_owner(message.from_user.id):
        return
    user, error = await resolve_user_safe(message.text)
    if not user:
        await message.answer(error, reply_markup=cancel_kb(), parse_mode="HTML")
        return

    label = format_user_label(user)
    expires = await get_subscription_expires(user["user_id"])
    banned = await is_banned(user["user_id"])
    profile = await get_profile(user["user_id"])
    await state.clear()

    if expires:
        active = "✅ Активна" if expires > datetime.utcnow() else "❌ Истекла"
        sub_text = f"{active} (до {expires.strftime('%d.%m.%Y')})"
    else:
        sub_text = "❌ Нет"

    if profile:
        g = str(profile.get("gender", "")).lower()
        gender_label = "👨 Мужской" if g in {"м", "male", "man"} else "👩 Женский"
        profile_text = (
            f"\n\n📋 <b>Анкета:</b>\n"
            f"  Имя: {profile['name']}\n"
            f"  Возраст: {profile['age']}\n"
            f"  Пол: {gender_label}"
        )
    else:
        profile_text = "\n\n📋 Анкеты нет"

    text = (
        f"🔍 <b>{label}</b>\n\n"
        f"💳 Подписка: {sub_text}\n"
        f"🚫 Бан: {'Да' if banned else 'Нет'}\n"
        f"🌍 Страна: {user.get('country', '—')}\n"
        f"{profile_text}"
    )
    await message.answer(text, reply_markup=admin_main_kb(), parse_mode="HTML")


@router.callback_query(F.data == "adm_bans")
async def adm_bans(call: CallbackQuery) -> None:
    if not is_owner(call.from_user.id):
        await call.answer()
        return
    await call.answer()
    await call.message.edit_text(
        "🔒 <b>Управление банами</b>",
        reply_markup=bans_kb(), parse_mode="HTML",
    )


@router.callback_query(F.data == "adm_ban")
async def adm_ban_start(call: CallbackQuery, state: FSMContext) -> None:
    if not is_owner(call.from_user.id):
        await call.answer()
        return
    await call.answer()
    await state.set_state(AdminStates.waiting_ban_username)
    await call.message.edit_text(
        "🚫 <b>Забанить пользователя</b>\n\nВведи @username:",
        reply_markup=cancel_kb(), parse_mode="HTML",
    )


@router.message(AdminStates.waiting_ban_username)
async def adm_ban_username(message: Message, state: FSMContext) -> None:
    if not is_owner(message.from_user.id):
        return
    user, error = await resolve_user_safe(message.text)
    if not user:
        await message.answer(error, reply_markup=cancel_kb(), parse_mode="HTML")
        return

    label = format_user_label(user)
    if await is_banned(user["user_id"]):
        await state.clear()
        await message.answer(
            f"ℹ️ Пользователь <b>{label}</b> уже забанен.",
            reply_markup=admin_main_kb(), parse_mode="HTML",
        )
        return

    await state.update_data(target_id=user["user_id"], target_label=label)
    await state.set_state(AdminStates.waiting_ban_reason)
    await message.answer(
        f"🚫 Баним: <b>{label}</b>\n\nВведи причину бана:",
        reply_markup=cancel_kb(), parse_mode="HTML",
    )


@router.message(AdminStates.waiting_ban_reason)
async def adm_ban_reason(message: Message, state: FSMContext) -> None:
    if not is_owner(message.from_user.id):
        return

    reason = (message.text or "").strip()
    data = await state.get_data()
    target_id = data["target_id"]
    target_label = data["target_label"]

    await ban_user(user_id=target_id, banned_by=message.from_user.id, reason=reason)
    await state.clear()
    await message.answer(
        f"🚫 <b>{target_label}</b> забанен.\n📝 Причина: {reason}",
        reply_markup=admin_main_kb(), parse_mode="HTML",
    )
    try:
        await message.bot.send_message(
            target_id,
            f"🚫 Ты заблокирован в боте.\n📝 Причина: {reason}",
        )
    except Exception:
        pass


@router.callback_query(F.data == "adm_unban")
async def adm_unban_start(call: CallbackQuery, state: FSMContext) -> None:
    if not is_owner(call.from_user.id):
        await call.answer()
        return
    await call.answer()
    await state.set_state(AdminStates.waiting_unban)
    await call.message.edit_text(
        "✅ <b>Разбанить пользователя</b>\n\nВведи @username:",
        reply_markup=cancel_kb(), parse_mode="HTML",
    )


@router.message(AdminStates.waiting_unban)
async def adm_unban_do(message: Message, state: FSMContext) -> None:
    if not is_owner(message.from_user.id):
        return
    user, error = await resolve_user_safe(message.text)
    if not user:
        await message.answer(error, reply_markup=cancel_kb(), parse_mode="HTML")
        return

    label = format_user_label(user)

    if not await is_banned(user["user_id"]):
        await state.clear()
        await message.answer(
            f"ℹ️ Пользователь <b>{label}</b> не забанен.",
            reply_markup=admin_main_kb(), parse_mode="HTML",
        )
        return

    await unban_user(user["user_id"])
    await state.clear()
    await message.answer(
        f"✅ <b>{label}</b> разбанен.",
        reply_markup=admin_main_kb(), parse_mode="HTML",
    )
    try:
        await message.bot.send_message(user["user_id"], "✅ Твой доступ в боте восстановлен.")
    except Exception:
        pass


@router.callback_query(F.data == "adm_banlist")
async def adm_banlist(call: CallbackQuery) -> None:
    if not is_owner(call.from_user.id):
        await call.answer()
        return
    await call.answer()

    banned = await get_banned_list()
    if not banned:
        await call.message.edit_text(
            "🚫 <b>Список банов пуст</b>",
            reply_markup=back_kb(), parse_mode="HTML",
        )
        return

    lines = ["🚫 <b>Забаненные пользователи:</b>\n"]
    for b in banned[:20]:
        uname = f"@{b['username']}" if b.get("username") else f"id:{b['user_id']}"
        reason = b.get("reason") or "без причины"
        dt = (b.get("banned_at") or "")[:10]
        lines.append(f"• {uname} — {reason} <i>({dt})</i>")

    if len(banned) > 20:
        lines.append(f"\n<i>...и ещё {len(banned) - 20}</i>")

    await call.message.edit_text(
        "\n".join(lines),
        reply_markup=back_kb(), parse_mode="HTML",
    )
