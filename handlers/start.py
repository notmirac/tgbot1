# handlers/start.py
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import config
from database import (
    add_or_update_user,
    has_active_subscription,
    get_subscription_expires,
    has_profile,
    is_banned,
    get_user_lang,
    set_user_lang,
)
from keyboards import buy_access_keyboard, main_menu_keyboard, language_keyboard
from states import ChatStates
from utils.i18n import tr, is_button, normalize_lang

logger = logging.getLogger(__name__)
router = Router()

# Защита от дублей /start — храним время последнего выполнения
_start_processed: dict[int, float] = {}


def _price_label(lang: str) -> str:
    return "300 руб." if normalize_lang(lang) == "ru" else "$3.00"


async def _reset_to_home(message: Message, state: FSMContext, lang: str) -> None:
    await state.clear()
    await state.set_state(ChatStates.main_menu)
    await message.answer(
        tr(lang, "hello", name=message.from_user.first_name) + "\n\n" + tr(lang, "home"),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(Command("start", "sstart"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    import time
    user_id = message.from_user.id
    now     = time.monotonic()

    # ИСПРАВЛЕНО: дополнительная защита от дублей на уровне хендлера
    # Если /start пришёл менее чем 3 сек назад — игнорируем
    last = _start_processed.get(user_id, 0)
    if now - last < 3.0:
        logger.debug("Duplicate /start ignored for user %d", user_id)
        return
    _start_processed[user_id] = now

    try:
        if await is_banned(user_id):
            lang = await get_user_lang(user_id)
            await message.answer(tr(lang, "banned"))
            return
    except Exception as e:
        logger.error("is_banned error user=%d: %s", user_id, e)

    try:
        await add_or_update_user(
            user_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            language_code=(message.from_user.language_code or "ru"),
        )
    except Exception as e:
        logger.error("add_or_update_user error user=%d: %s", user_id, e)

    try:
        lang = await get_user_lang(user_id)
    except Exception as e:
        logger.error("get_user_lang error user=%d: %s", user_id, e)
        lang = "ru"

    # Если язык не выбран — показываем выбор языка
    if not lang:
        await message.answer(tr("ru", "start_choose_lang"), reply_markup=language_keyboard())
        await state.clear()
        return

    await _reset_to_home(message, state, lang)
    logger.info("User %d started bot (lang=%s)", user_id, lang)


@router.message(lambda msg: is_button(msg.text, "home"))
async def btn_home(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await _reset_to_home(message, state, lang)


@router.message(lambda msg: is_button(msg.text, "status"))
async def btn_subscription_status(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    lang    = await get_user_lang(user_id)
    try:
        await state.set_state(ChatStates.main_menu)
        if await has_active_subscription(user_id):
            expires     = await get_subscription_expires(user_id)
            expires_str = expires.strftime("%d.%m.%Y") if expires else "—"
            await message.answer(
                tr(lang, "sub_active", date=expires_str),
                reply_markup=main_menu_keyboard(lang),
                parse_mode="HTML",
            )
        else:
            await message.answer(
                tr(lang, "sub_none"),
                reply_markup=buy_access_keyboard(_price_label(lang), lang),
                parse_mode="HTML",
            )
    except Exception as e:
        logger.error("btn_status error user=%d: %s", user_id, e)
        await message.answer(
            "⚠️ Ошибка. Попробуй ещё раз." if normalize_lang(lang) == "ru"
            else "⚠️ Error. Try again.",
            reply_markup=main_menu_keyboard(lang),
        )


@router.message(lambda msg: is_button(msg.text, "language"))
async def btn_language(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await state.set_state(ChatStates.main_menu)
    await message.answer(tr(lang, "lang_choose"), reply_markup=language_keyboard())


@router.callback_query(F.data == "lang_ru")
async def set_lang_ru(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        await set_user_lang(callback.from_user.id, "ru")
        await callback.answer("✅ Русский")
        try:
            await callback.message.edit_text(tr("ru", "lang_set_ru"))
        except Exception:
            pass
        await state.clear()
        await state.set_state(ChatStates.main_menu)
        await callback.message.answer(
            tr("ru", "home"), reply_markup=main_menu_keyboard("ru"), parse_mode="HTML"
        )
    except Exception as e:
        logger.error("set_lang_ru error: %s", e)
        await callback.answer()


@router.callback_query(F.data == "lang_en")
async def set_lang_en(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        await set_user_lang(callback.from_user.id, "en")
        await callback.answer("✅ English")
        try:
            await callback.message.edit_text(tr("en", "lang_set_en"))
        except Exception:
            pass
        await state.clear()
        await state.set_state(ChatStates.main_menu)
        await callback.message.answer(
            tr("en", "home"), reply_markup=main_menu_keyboard("en"), parse_mode="HTML"
        )
    except Exception as e:
        logger.error("set_lang_en error: %s", e)
        await callback.answer()


# ── Поддержка ─────────────────────────────────────────────────

@router.message(lambda msg: is_button(msg.text, "support"))
async def support_entry(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await state.clear()
    await state.set_state(ChatStates.waiting_support_message)
    await message.answer(
        tr(lang, "support_intro"),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )


@router.message(ChatStates.waiting_support_message)
async def support_send(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)

    if is_button(message.text, "home") or is_button(message.text, "back"):
        await _reset_to_home(message, state, lang)
        return

    text = (message.text or "").strip()
    if not text:
        await message.answer(tr(lang, "support_empty"), reply_markup=main_menu_keyboard(lang))
        return

    try:
        from handlers.admin import reply_kb
        await message.bot.send_message(
            config.admin_id,
            f"📩 <b>Сообщение в поддержку</b>\n\n"
            f"От: {message.from_user.full_name}\n"
            f"ID: <code>{message.from_user.id}</code>\n"
            f"Username: @{message.from_user.username or '-'}\n"
            f"Язык: {lang}\n\n{text}",
            reply_markup=reply_kb(message.from_user.id),
            parse_mode="HTML",
        )
    except Exception as e:
        logger.error("support send failed: %s", e)
        await state.clear()
        await state.set_state(ChatStates.main_menu)
        await message.answer(tr(lang, "support_failed"), reply_markup=main_menu_keyboard(lang))
        return

    await state.clear()
    await state.set_state(ChatStates.main_menu)
    await message.answer(tr(lang, "support_sent"), reply_markup=main_menu_keyboard(lang))
