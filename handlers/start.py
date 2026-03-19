# handlers/start.py
import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from database import (
    add_or_update_user, has_active_subscription,
    get_subscription_expires, has_profile, is_banned,
    get_user_lang, set_user_lang,
)
from keyboards import (
    BTN_HOME, BTN_STATUS,
    buy_access_keyboard, main_menu_keyboard, language_keyboard,
    BTN_LANGUAGE,
)
from states import ChatStates
from config import config

logger = logging.getLogger(__name__)
router = Router()

# Тексты на двух языках
TEXTS = {
    "ru": {
        "hello": "Привет, <b>{name}</b>! 👋\n\nВыбери раздел в меню ниже:",
        "no_profile": "\n\n👤 Создай <b>анкету</b> — нажми «👤 Моя анкета».",
        "banned": "🚫 Ты заблокирован в боте.",
        "home": (
            "🏠 <b>Главная страница</b>\n\n"
            "• 👤 <b>Моя анкета</b>\n"
            "• 🔞 <b>Чат 18+</b> (платно)\n"
            "• 🖼 <b>Фото 18+</b> (платно)\n"
            "• 💳 <b>Моя подписка</b>\n"
            "• 🌐 <b>Язык</b>\n\nВыбирай! 👇"
        ),
        "sub_active": "💳 <b>Подписка активна</b>\n📅 До: <b>{date}</b>\n\nВсе разделы доступны 🎉",
        "sub_none": "💳 <b>Нет подписки</b>\n\nКупи доступ 👇",
        "lang_choose": "🌐 Выбери язык:",
        "lang_set": "✅ Язык изменён на Русский 🇷🇺",
    },
    "en": {
        "hello": "Hello, <b>{name}</b>! 👋\n\nChoose a section below:",
        "no_profile": "\n\n👤 Create a <b>profile</b> — tap «👤 My Profile».",
        "banned": "🚫 You are blocked.",
        "home": (
            "🏠 <b>Main menu</b>\n\n"
            "• 👤 <b>My Profile</b>\n"
            "• 🔞 <b>Chat 18+</b> (paid)\n"
            "• 🖼 <b>Photos 18+</b> (paid)\n"
            "• 💳 <b>My Subscription</b>\n"
            "• 🌐 <b>Language</b>\n\nChoose! 👇"
        ),
        "sub_active": "💳 <b>Subscription active</b>\n📅 Until: <b>{date}</b>\n\nAll sections available 🎉",
        "sub_none": "💳 <b>No subscription</b>\n\nBuy access 👇",
        "lang_choose": "🌐 Choose language:",
        "lang_set": "✅ Language set to English 🇬🇧",
    },
}


def _price_label() -> str:
    if config.currency == "RUB":
        return f"{config.subscription_price // 100} руб."
    return f"{config.subscription_price / 100:.2f} {config.currency}"


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    if await is_banned(user_id):
        await message.answer("🚫 Ты заблокирован в боте.")
        return

    await state.clear()
    await state.set_state(ChatStates.main_menu)

    await add_or_update_user(
        user_id=user_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        language_code=message.from_user.language_code,
    )

    lang  = await get_user_lang(user_id)
    t     = TEXTS[lang]
    has_p = await has_profile(user_id)
    hint  = t["no_profile"] if not has_p else ""

    await message.answer(
        t["hello"].format(name=message.from_user.first_name) + hint,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(lambda msg: msg.text == BTN_HOME)
async def btn_home(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    if await is_banned(user_id):
        await message.answer("🚫 Ты заблокирован.")
        return
    await add_or_update_user(
        user_id=user_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        language_code=message.from_user.language_code,
    )
    await state.set_state(ChatStates.main_menu)
    lang = await get_user_lang(user_id)
    await message.answer(
        TEXTS[lang]["home"],
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(lambda msg: msg.text == BTN_STATUS)
async def btn_subscription_status(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    lang    = await get_user_lang(user_id)
    t       = TEXTS[lang]
    try:
        if await has_active_subscription(user_id):
            expires     = await get_subscription_expires(user_id)
            expires_str = expires.strftime("%d.%m.%Y") if expires else "—"
            await message.answer(
                t["sub_active"].format(date=expires_str),
                reply_markup=main_menu_keyboard(), parse_mode="HTML",
            )
        else:
            await message.answer(
                t["sub_none"],
                reply_markup=buy_access_keyboard(_price_label()),
                parse_mode="HTML",
            )
    except Exception as e:
        logger.error("btn_status error: %s", e)
        await message.answer("⚠️ Ошибка. Попробуй ещё раз.", reply_markup=main_menu_keyboard())


# ── Выбор языка ───────────────────────────────────────────────

@router.message(lambda msg: msg.text == BTN_LANGUAGE)
async def btn_language(message: Message) -> None:
    lang = await get_user_lang(message.from_user.id)
    await message.answer(
        TEXTS[lang]["lang_choose"],
        reply_markup=language_keyboard(),
    )


@router.callback_query(F.data == "lang_ru")
async def set_lang_ru(callback: CallbackQuery) -> None:
    await set_user_lang(callback.from_user.id, "ru")
    await callback.answer("✅ Русский")
    await callback.message.edit_text(TEXTS["ru"]["lang_set"])


@router.callback_query(F.data == "lang_en")
async def set_lang_en(callback: CallbackQuery) -> None:
    await set_user_lang(callback.from_user.id, "en")
    await callback.answer("✅ English")
    await callback.message.edit_text(TEXTS["en"]["lang_set"])
