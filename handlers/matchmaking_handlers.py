# handlers/matchmaking.py
# ────────────────────────────────────────────────────────────
#  Поиск собеседника, живой чат, завершение чата.
# ────────────────────────────────────────────────────────────

import logging

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import get_profile, has_active_subscription, has_profile
from keyboards import (
    BTN_SEARCH, BTN_SEARCH18, BTN_END_CHAT,
    live_chat_keyboard, main_menu_keyboard, buy_access_keyboard,
)
from services import matchmaking as mm
from states import ChatStates
from config import config

logger = logging.getLogger(__name__)
router = Router()


def _price_label() -> str:
    if config.currency == "RUB":
        return f"{config.subscription_price // 100} руб."
    return f"{config.subscription_price / 100:.2f} {config.currency}"


# ══════════════════════════════════════════════════════════════
#  ПОИСК ОБЫЧНОГО СОБЕСЕДНИКА
# ══════════════════════════════════════════════════════════════

@router.message(lambda msg: msg.text == BTN_SEARCH)
async def start_search_normal(message: Message, state: FSMContext) -> None:
    """Кнопка «🔍 Найти собеседника» — обычный чат."""
    user_id = message.from_user.id

    # Проверяем анкету
    if not await has_profile(user_id):
        await message.answer(
            "👤 Для поиска собеседника нужна анкета!\n\n"
            "Нажми <b>👤 Моя анкета</b> чтобы создать её.",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
        return

    # Если уже в чате или очереди
    if mm.is_in_chat(user_id):
        await message.answer("❗ Ты уже в чате. Сначала заверши его.", reply_markup=live_chat_keyboard())
        return
    if mm.is_in_queue(user_id):
        await message.answer("⏳ Ты уже в очереди поиска. Подожди немного...")
        return

    # Ищем партнёра
    partner_id = mm.find_partner(user_id, mode="normal")

    if partner_id:
        # Нашли пару!
        mm.create_pair(user_id, partner_id)

        profile_me      = await get_profile(user_id)
        profile_partner = await get_profile(partner_id)

        gender_label = {"м": "👨 Мужской", "ж": "👩 Женский"}

        # Уведомляем обоих
        await message.answer(
            f"🎉 <b>Собеседник найден!</b>\n\n"
            f"👤 {profile_partner['name']}, {profile_partner['age']} лет, "
            f"{gender_label.get(profile_partner['gender'], '')}\n\n"
            "Можешь писать! Для завершения нажми ❌",
            reply_markup=live_chat_keyboard(),
            parse_mode="HTML",
        )
        await message.bot.send_message(
            partner_id,
            f"🎉 <b>Собеседник найден!</b>\n\n"
            f"👤 {profile_me['name']}, {profile_me['age']} лет, "
            f"{gender_label.get(profile_me['gender'], '')}\n\n"
            "Можешь писать! Для завершения нажми ❌",
            reply_markup=live_chat_keyboard(),
            parse_mode="HTML",
        )

        await state.set_state(ChatStates.in_chat)

    else:
        # Никого нет — добавляем в очередь
        mm.add_to_queue(user_id, mode="normal")
        await state.set_state(ChatStates.searching)
        size = mm.queue_size("normal")
        await message.answer(
            f"⏳ <b>Ищем собеседника...</b>\n\n"
            f"В очереди: {size} чел.\n\n"
            "Как только кто-то появится — соединим автоматически!\n"
            "Нажми ❌ чтобы отменить поиск.",
            reply_markup=live_chat_keyboard(),
            parse_mode="HTML",
        )


# ══════════════════════════════════════════════════════════════
#  ПОИСК СОБЕСЕДНИКА 18+
# ══════════════════════════════════════════════════════════════

@router.message(lambda msg: msg.text == BTN_SEARCH18)
async def start_search_adult(message: Message, state: FSMContext) -> None:
    """Кнопка «🔞 Найти собеседника 18+»."""
    user_id = message.from_user.id

    # Проверяем анкету
    profile = await get_profile(user_id)
    if not profile:
        await message.answer(
            "👤 Для поиска нужна анкета!\n"
            "Нажми <b>👤 Моя анкета</b> чтобы создать её.",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
        return

    # Проверяем возраст
    if profile["age"] < 18:
        await message.answer(
            "🔞 Раздел 18+ недоступен.\n"
            f"Тебе {profile['age']} лет — этот раздел только для совершеннолетних.",
            reply_markup=main_menu_keyboard(),
        )
        return

    # Проверяем подписку
    if not await has_active_subscription(user_id):
        await message.answer(
            "🔒 Для поиска в 18+ нужна активная подписка.\n\n"
            f"Стоимость: <b>{_price_label()}</b>",
            reply_markup=buy_access_keyboard(_price_label()),
            parse_mode="HTML",
        )
        return

    if mm.is_in_chat(user_id):
        await message.answer("❗ Ты уже в чате. Сначала заверши его.", reply_markup=live_chat_keyboard())
        return
    if mm.is_in_queue(user_id):
        await message.answer("⏳ Ты уже в очереди поиска.")
        return

    partner_id = mm.find_partner(user_id, mode="adult")

    if partner_id:
        mm.create_pair(user_id, partner_id)
        profile_partner = await get_profile(partner_id)
        gender_label = {"м": "👨 Мужской", "ж": "👩 Женский"}

        await message.answer(
            f"🎉 <b>Собеседник найден!</b> 🔞\n\n"
            f"👤 {profile_partner['name']}, {profile_partner['age']} лет, "
            f"{gender_label.get(profile_partner['gender'], '')}\n\n"
            "Можешь писать! 🔥",
            reply_markup=live_chat_keyboard(),
            parse_mode="HTML",
        )
        await message.bot.send_message(
            partner_id,
            f"🎉 <b>Собеседник найден!</b> 🔞\n\n"
            f"👤 {profile['name']}, {profile['age']} лет, "
            f"{gender_label.get(profile['gender'], '')}\n\n"
            "Можешь писать! 🔥",
            reply_markup=live_chat_keyboard(),
            parse_mode="HTML",
        )
        await state.set_state(ChatStates.in_chat)

    else:
        mm.add_to_queue(user_id, mode="adult")
        await state.set_state(ChatStates.searching)
        size = mm.queue_size("adult")
        await message.answer(
            f"⏳ <b>Ищем собеседника 18+...</b>\n\n"
            f"В очереди: {size} чел.\n\n"
            "Как только кто-то появится — соединим!\n"
            "Нажми ❌ чтобы отменить.",
            reply_markup=live_chat_keyboard(),
            parse_mode="HTML",
        )


# ══════════════════════════════════════════════════════════════
#  ЖИВОЙ ЧАТ — пересылка сообщений
# ══════════════════════════════════════════════════════════════

@router.message(ChatStates.in_chat)
async def relay_message(message: Message, state: FSMContext) -> None:
    """Пересылаем сообщение собеседнику."""
    user_id = message.from_user.id

    # Кнопка завершения
    if message.text == BTN_END_CHAT:
        await end_chat_handler(message, state)
        return

    partner_id = mm.get_partner(user_id)
    if not partner_id:
        await state.set_state(ChatStates.main_menu)
        await message.answer(
            "❌ Чат завершён.",
            reply_markup=main_menu_keyboard(),
        )
        return

    # Пересылаем разные типы сообщений
    try:
        if message.text:
            await message.bot.send_message(partner_id, message.text)
        elif message.photo:
            await message.bot.send_photo(partner_id, message.photo[-1].file_id, caption=message.caption or "")
        elif message.video:
            await message.bot.send_video(partner_id, message.video.file_id, caption=message.caption or "")
        elif message.voice:
            await message.bot.send_voice(partner_id, message.voice.file_id)
        elif message.sticker:
            await message.bot.send_sticker(partner_id, message.sticker.file_id)
        else:
            await message.answer("⚠️ Этот тип сообщений не поддерживается.")
    except Exception as exc:
        logger.error("Relay error user=%d partner=%d: %s", user_id, partner_id, exc)
        await message.answer("⚠️ Не удалось доставить сообщение. Собеседник мог заблокировать бота.")


# ══════════════════════════════════════════════════════════════
#  ОЧЕРЕДЬ ПОИСКА — отмена
# ══════════════════════════════════════════════════════════════

@router.message(ChatStates.searching)
async def cancel_search(message: Message, state: FSMContext) -> None:
    """В режиме поиска — только отмена."""
    if message.text == BTN_END_CHAT:
        mm.remove_from_queue(message.from_user.id)
        await state.set_state(ChatStates.main_menu)
        await message.answer("🔍 Поиск отменён.", reply_markup=main_menu_keyboard())
    else:
        await message.answer("⏳ Ищем собеседника... Нажми ❌ чтобы отменить.", reply_markup=live_chat_keyboard())


# ══════════════════════════════════════════════════════════════
#  ЗАВЕРШЕНИЕ ЧАТА
# ══════════════════════════════════════════════════════════════

async def end_chat_handler(message: Message, state: FSMContext) -> None:
    """Завершить активный чат — уведомить обоих участников."""
    user_id = message.from_user.id
    partner_id = mm.end_chat(user_id)

    await state.set_state(ChatStates.main_menu)
    await message.answer(
        "❌ <b>Чат завершён.</b>\n\nВозвращайся когда захочешь! 👋",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )

    # Уведомляем партнёра
    if partner_id:
        try:
            await message.bot.send_message(
                partner_id,
                "❌ <b>Собеседник завершил чат.</b>\n\nМожешь найти нового! 🔍",
                reply_markup=main_menu_keyboard(),
                parse_mode="HTML",
            )
        except Exception as exc:
            logger.error("Could not notify partner %d: %s", partner_id, exc)

    logger.info("Chat ended by user=%d", user_id)
