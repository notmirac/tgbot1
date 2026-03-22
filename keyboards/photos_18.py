# handlers/photos_18.py
# ────────────────────────────────────────────────────────────
#  Раздел «Анкеты 18+» — листание анкет с кнопками ◀️ ▶️
#  Анкеты хранятся в data/profiles_data.py
#  Чтобы добавить фото — замени "" на URL или file_id
# ────────────────────────────────────────────────────────────

import logging
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from config import config
from database import has_active_subscription, get_user_lang
from keyboards import buy_access_keyboard, main_menu_keyboard, profiles_browse_keyboard
from states import ChatStates
from utils.i18n import is_button

logger = logging.getLogger(__name__)
router = Router()


def _price_label(lang: str) -> str:
    try:
        if lang == "ru":
            return f"{config.subscription_price_rub // 100} руб."
        return f"${config.subscription_price_usd / 100:.2f}"
    except Exception:
        return "300 руб."


def _get_profiles():
    """Загружаем анкеты — с защитой от ошибки импорта."""
    try:
        from data.profiles_data import PROFILES_18
        return PROFILES_18
    except Exception as e:
        logger.error("Cannot load PROFILES_18: %s", e)
        return []


def _profile_text(p: dict, index: int, total: int, lang: str) -> str:
    if lang == "ru":
        return (
            f"👤 <b>{p['name']}</b>, {p['age']} лет\n"
            f"📍 {p.get('city', '—')}\n\n"
            f"💬 {p.get('about', '—')}\n\n"
            f"<i>{index + 1} из {total}</i>"
        )
    return (
        f"👤 <b>{p['name']}</b>, {p['age']} y.o.\n"
        f"📍 {p.get('city', '—')}\n\n"
        f"💬 {p.get('about', '—')}\n\n"
        f"<i>{index + 1} of {total}</i>"
    )


async def _send_profile_message(target, index: int, lang: str, edit: bool = False) -> None:
    """
    Отправить или обновить карточку анкеты.
    target — Message или CallbackQuery.
    ИСПРАВЛЕНО: отдельная обработка edit и send, try/except на каждом шаге.
    """
    profiles = _get_profiles()
    if not profiles:
        msg = target.message if isinstance(target, CallbackQuery) else target
        await msg.answer(
            "🖼 Анкеты пока не добавлены." if lang == "ru" else "🖼 No profiles yet.",
            reply_markup=main_menu_keyboard(lang),
        )
        return

    total     = len(profiles)
    index     = max(0, min(index, total - 1))
    p         = profiles[index]
    text      = _profile_text(p, index, total, lang)
    kb        = profiles_browse_keyboard(index, total, lang)
    has_photo = bool((p.get("photo") or "").strip())

    if edit and isinstance(target, CallbackQuery):
        msg = target.message
        try:
            if has_photo:
                await msg.edit_media(
                    media=InputMediaPhoto(media=p["photo"], caption=text, parse_mode="HTML"),
                    reply_markup=kb,
                )
            else:
                await msg.edit_text(text, reply_markup=kb, parse_mode="HTML")
            return
        except TelegramBadRequest as e:
            # Если сообщение не изменилось — просто игнорируем
            if "message is not modified" in str(e).lower():
                return
            logger.warning("edit failed, sending new: %s", e)
        except Exception as e:
            logger.warning("edit error: %s", e)

    # Отправляем новое сообщение
    send_target = target.message if isinstance(target, CallbackQuery) else target
    try:
        if has_photo:
            await send_target.answer_photo(
                photo=p["photo"],
                caption=text,
                reply_markup=kb,
                parse_mode="HTML",
            )
        else:
            await send_target.answer(text, reply_markup=kb, parse_mode="HTML")
    except Exception as e:
        logger.error("send_profile error index=%d: %s", index, e)
        await send_target.answer(
            "⚠️ Не удалось загрузить анкету. Попробуй следующую." if lang == "ru"
            else "⚠️ Failed to load profile. Try next.",
            reply_markup=kb,
        )


# ── Кнопка «Анкеты 18+» ──────────────────────────────────────

@router.message(lambda msg: is_button(msg.text, "photo18"))
async def open_photos_18(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)

    # Проверка подписки
    try:
        has_sub = await has_active_subscription(message.from_user.id)
    except Exception as e:
        logger.error("has_active_subscription error: %s", e)
        has_sub = False

    if not has_sub:
        price = _price_label(lang)
        title = (
            "🖼 <b>Анкеты 18+</b>\n\n🔒 Раздел доступен только по подписке."
            if lang == "ru" else
            "🖼 <b>Profiles 18+</b>\n\n🔒 Available with subscription only."
        )
        await message.answer(
            f"{title}\n\n{'Стоимость' if lang == 'ru' else 'Price'}: <b>{price}</b>",
            reply_markup=buy_access_keyboard(price, lang),
            parse_mode="HTML",
        )
        return

    profiles = _get_profiles()
    if not profiles:
        await message.answer(
            "🖼 Анкеты пока не добавлены." if lang == "ru" else "🖼 No profiles yet.",
            reply_markup=main_menu_keyboard(lang),
        )
        return

    await state.set_state(ChatStates.browsing_profiles)
    await state.update_data(browse_index=0)
    await _send_profile_message(message, 0, lang, edit=False)


# ── Листание ◀️ ▶️ ───────────────────────────────────────────

@router.callback_query(F.data.startswith("profile_browse:"))
async def browse_profile(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_user_lang(callback.from_user.id)

    try:
        index = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        await callback.answer()
        return

    profiles = _get_profiles()
    if not profiles:
        await callback.answer()
        return

    index = max(0, min(index, len(profiles) - 1))
    await state.update_data(browse_index=index)
    await callback.answer()
    await _send_profile_message(callback, index, lang, edit=True)


# ── Счётчик «1 / 75» — просто заглушка ──────────────────────

@router.callback_query(F.data == "profile_browse_noop")
async def browse_noop(callback: CallbackQuery) -> None:
    await callback.answer()


# ── Кнопка «Написать» ────────────────────────────────────────

@router.callback_query(F.data.startswith("profile_write:"))
async def profile_write(callback: CallbackQuery, state: FSMContext) -> None:
    lang     = await get_user_lang(callback.from_user.id)
    profiles = _get_profiles()

    try:
        index = int(callback.data.split(":")[1])
        p     = profiles[index]
    except (IndexError, ValueError):
        await callback.answer("Ошибка" if lang == "ru" else "Error", show_alert=True)
        return

    await callback.answer()

    # Создаём виртуального партнёра из анкеты
    partner = {
        "name":     p["name"],
        "age":      p["age"],
        "gender":   "ж",
        "city":     p.get("city", ""),
        "interest": p.get("about", ""),
        "lang":     lang,
    }

    await state.update_data(virtual_partner=partner, history_18=[])
    await state.set_state(ChatStates.chat_18)

    from keyboards import live_chat_keyboard
    await callback.message.answer(
        (f"Начинаем чат с <b>{p['name']}</b> 😊\n\nНапиши что-нибудь!"
         if lang == "ru" else
         f"Starting chat with <b>{p['name']}</b> 😊\n\nSay something!"),
        reply_markup=live_chat_keyboard(lang),
        parse_mode="HTML",
    )


# ── Кнопка «Закрыть» ─────────────────────────────────────────

@router.callback_query(F.data == "profile_close")
async def profile_close(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await get_user_lang(callback.from_user.id)
    await state.set_state(ChatStates.main_menu)
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer(
        "Вернулся в меню 📌" if lang == "ru" else "Back to menu 📌",
        reply_markup=main_menu_keyboard(lang),
    )
