import asyncio
import logging
import random

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import config
from database import (
    get_partner_preferences,
    get_profile,
    has_active_subscription,
    set_partner_preferences,
)
from keyboards import (
    BTN_AGE_18_25,
    BTN_AGE_26_30,
    BTN_AGE_31_35,
    BTN_AGE_36_40,
    BTN_AGE_41_45,
    BTN_AGE_46_50,
    BTN_BACK,
    BTN_CHAT18,
    BTN_END_CHAT,
    BTN_FEMALE,
    BTN_MALE,
    age_range_keyboard,
    buy_access_keyboard,
    gender_keyboard,
    live_chat_keyboard,
    main_menu_keyboard,
)
from services import build_virtual_profile, get_virtual_reply
from states import ChatStates
from utils.chat_logger import log_chat_event, log_chat_message

logger = logging.getLogger(__name__)
router = Router()
MAX_HISTORY_PAIRS = 12
AGE_RANGES = {
    BTN_AGE_18_25: (18, 25),
    BTN_AGE_26_30: (26, 30),
    BTN_AGE_31_35: (31, 35),
    BTN_AGE_36_40: (36, 40),
    BTN_AGE_41_45: (41, 45),
    BTN_AGE_46_50: (46, 50),
}
GENDER_MAP = {BTN_MALE: "м", BTN_FEMALE: "ж"}


def _price_label() -> str:
    if config.currency == "RUB":
        return f"{config.subscription_price // 100} руб."
    return f"{config.subscription_price / 100:.2f} {config.currency}"


@router.message(lambda msg: msg.text == BTN_CHAT18)
async def enter_chat_18(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    profile = await get_profile(user_id)

    if not profile:
        await message.answer(
            "👤 Для этого раздела нужна анкета.\nНажми «👤 Моя анкета», чтобы создать её.",
            reply_markup=main_menu_keyboard(),
        )
        return

    if profile["age"] < 18:
        await message.answer(
            f"🔞 Этот раздел только для совершеннолетних.\nТебе {profile['age']} лет — доступ закрыт.",
            reply_markup=main_menu_keyboard(),
        )
        return

    if not await has_active_subscription(user_id):
        await message.answer(
            "🔞 <b>Чат 18+</b>\n\n"
            "🔒 Этот раздел доступен только по подписке.\n\n"
            f"Стоимость: <b>{_price_label()}</b>",
            reply_markup=buy_access_keyboard(_price_label()),
            parse_mode="HTML",
        )
        return

    await state.clear()
    await state.set_state(ChatStates.waiting_partner_gender)
    prefs = await get_partner_preferences(user_id)
    hint = "👩 Женский" if prefs["preferred_gender"] == "ж" else "👨 Мужской"
    await message.answer(
        f"Кого ищем?\n\nСейчас выбран: <b>{hint}</b>",
        reply_markup=gender_keyboard(),
        parse_mode="HTML",
    )


@router.message(ChatStates.waiting_partner_gender)
async def choose_partner_gender(message: Message, state: FSMContext) -> None:
    if message.text == BTN_BACK:
        await state.set_state(ChatStates.main_menu)
        await message.answer("Вернулся в меню 🏠", reply_markup=main_menu_keyboard())
        return

    if message.text not in GENDER_MAP:
        await message.answer("Выбери пол кнопкой ниже.", reply_markup=gender_keyboard())
        return

    preferred_gender = GENDER_MAP[message.text]
    await state.update_data(preferred_gender=preferred_gender)
    await state.set_state(ChatStates.waiting_partner_age)
    await message.answer("Выбери возраст собеседника:", reply_markup=age_range_keyboard())


@router.message(ChatStates.waiting_partner_age)
async def choose_partner_age(message: Message, state: FSMContext) -> None:
    if message.text == BTN_BACK:
        await state.set_state(ChatStates.waiting_partner_gender)
        await message.answer("Кого ищем?", reply_markup=gender_keyboard())
        return

    if message.text not in AGE_RANGES:
        await message.answer("Выбери диапазон возраста кнопкой ниже.", reply_markup=age_range_keyboard())
        return

    age_min, age_max = AGE_RANGES[message.text]
    data = await state.get_data()
    preferred_gender = data.get("preferred_gender", "ж")
    await set_partner_preferences(message.from_user.id, preferred_gender, age_min, age_max)
    await state.update_data(preferred_age_min=age_min, preferred_age_max=age_max, history_18=[])
    await state.set_state(ChatStates.searching)

    approx_queue = random.randint(243, 267)
    await log_chat_event(message.from_user.id, message.from_user.username, "search_started", f"gender={preferred_gender} age={age_min}-{age_max}")
    await message.answer(
        "⏳ <b>Поиск собеседника...</b>\n\n"
        f"В очереди: примерно <b>{approx_queue}</b> человек\n\n"
        "Соединим автоматически через несколько секунд.",
        reply_markup=live_chat_keyboard(),
        parse_mode="HTML",
    )
    asyncio.create_task(_complete_search(message, state))


async def _complete_search(message: Message, state: FSMContext) -> None:
    await asyncio.sleep(random.uniform(5.0, 6.0))
    current_state = await state.get_state()
    if current_state != ChatStates.searching:
        return

    data = await state.get_data()
    partner = build_virtual_profile(
        preferred_gender=data.get("preferred_gender", "ж"),
        age_min=data.get("preferred_age_min", 18),
        age_max=data.get("preferred_age_max", 25),
    )
    await state.update_data(virtual_partner=partner, history_18=[])
    await state.set_state(ChatStates.chat_18)
    await log_chat_event(message.from_user.id, message.from_user.username, "partner_found", f"{partner['name']} {partner['age']} {partner['gender']}")
    await message.answer(
        f"🎉 <b>Собеседник найден</b>\n\n{partner['name']}, {partner['age']} лет\nМожешь начинать общение.",
        reply_markup=live_chat_keyboard(),
        parse_mode="HTML",
    )


@router.message(ChatStates.searching)
async def cancel_search(message: Message, state: FSMContext) -> None:
    if message.text == BTN_END_CHAT:
        await state.set_state(ChatStates.main_menu)
        await log_chat_event(message.from_user.id, message.from_user.username, "search_cancelled")
        await message.answer("Поиск остановлен.", reply_markup=main_menu_keyboard())
        return
    await message.answer("Ищем собеседника... Нажми «❌ Завершить чат», чтобы отменить.", reply_markup=live_chat_keyboard())


@router.message(ChatStates.chat_18)
async def process_chat_18_message(message: Message, state: FSMContext) -> None:
    if message.text == BTN_END_CHAT:
        await state.clear()
        await state.set_state(ChatStates.main_menu)
        await log_chat_event(message.from_user.id, message.from_user.username, "chat_ended")
        await message.answer("Пользователь завершил сеанс", reply_markup=main_menu_keyboard())
        return

    if not await has_active_subscription(message.from_user.id):
        await state.set_state(ChatStates.main_menu)
        await message.answer("❌ Подписка истекла.", reply_markup=buy_access_keyboard(_price_label()))
        return

    data = await state.get_data()
    partner = data.get("virtual_partner") or {"name": "Собеседник", "age": 22, "gender": "ж", "opener": "Привет 🙂"}
    history = data.get("history_18", [])

    await log_chat_message(message.from_user.id, message.from_user.username, partner["name"], partner["age"], "user", message.text or "")
    await message.bot.send_chat_action(message.chat.id, "typing")
    reply = await get_virtual_reply(message.text or "", partner, history=history, lang="ru")

    history.append({"role": "user", "content": message.text or ""})
    history.append({"role": "assistant", "content": reply})
    if len(history) > MAX_HISTORY_PAIRS * 2:
        history = history[-(MAX_HISTORY_PAIRS * 2):]

    await state.update_data(history_18=history)
    await log_chat_message(message.from_user.id, message.from_user.username, partner["name"], partner["age"], "partner", reply)
    await message.answer(reply, reply_markup=live_chat_keyboard())
