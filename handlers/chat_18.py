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
    get_user_lang,
)
from keyboards import (
    BTN_AGE_18_25,
    BTN_AGE_26_30,
    BTN_AGE_31_35,
    BTN_AGE_36_40,
    BTN_AGE_41_45,
    BTN_AGE_46_50,
    age_range_keyboard,
    buy_access_keyboard,
    gender_keyboard,
    live_chat_keyboard,
    main_menu_keyboard,
)
from services import build_virtual_profile, get_virtual_reply
from states import ChatStates
from utils.chat_logger import log_chat_event, log_chat_message
from utils.i18n import tr, is_button, gender_label

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

def _price_label() -> str:
    if config.currency == "RUB":
        return f"{config.subscription_price // 100} руб."
    return f"{config.subscription_price / 100:.2f} {config.currency}"

def _preferred_gender_from_text(text: str | None) -> str | None:
    if is_button(text, "male"):
        return "м"
    if is_button(text, "female"):
        return "ж"
    return None

@router.message(lambda msg: is_button(msg.text, "chat18"))
async def enter_chat_18(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    profile = await get_profile(user_id)

    if not profile:
        await message.answer(
            tr(lang, "chat18_need_profile"),
            reply_markup=main_menu_keyboard(lang),
        )
        return

    if profile["age"] < 18:
        await message.answer(
            tr(lang, "chat18_underage", age=profile["age"]),
            reply_markup=main_menu_keyboard(lang),
        )
        return

    if not await has_active_subscription(user_id):
        await message.answer(
            tr(lang, "chat18_need_sub", price=_price_label()),
            reply_markup=buy_access_keyboard(_price_label(), lang),
            parse_mode="HTML",
        )
        return

    await state.clear()
    await state.set_state(ChatStates.waiting_partner_gender)
    prefs = await get_partner_preferences(user_id)
    hint = gender_label(prefs["preferred_gender"], lang)
    await message.answer(
        f"{tr(lang, 'chat18_choose_gender')}\n\n{tr(lang, 'chat18_current_gender', gender=hint)}",
        reply_markup=gender_keyboard(lang),
        parse_mode="HTML",
    )

@router.message(ChatStates.waiting_partner_gender)
async def choose_partner_gender(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if is_button(message.text, "back"):
        await state.set_state(ChatStates.main_menu)
        await message.answer(tr(lang, "back_to_menu"), reply_markup=main_menu_keyboard(lang))
        return

    preferred_gender = _preferred_gender_from_text(message.text)
    if preferred_gender is None:
        await message.answer(tr(lang, "chat18_gender_invalid"), reply_markup=gender_keyboard(lang))
        return

    await state.update_data(preferred_gender=preferred_gender)
    await state.set_state(ChatStates.waiting_partner_age)
    await message.answer(tr(lang, "chat18_choose_age"), reply_markup=age_range_keyboard(lang))

@router.message(ChatStates.waiting_partner_age)
async def choose_partner_age(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if is_button(message.text, "back"):
        await state.set_state(ChatStates.waiting_partner_gender)
        await message.answer(tr(lang, "chat18_choose_gender"), reply_markup=gender_keyboard(lang))
        return

    if message.text not in AGE_RANGES:
        await message.answer(tr(lang, "chat18_age_invalid"), reply_markup=age_range_keyboard(lang))
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
        tr(lang, "chat18_searching", size=approx_queue),
        reply_markup=live_chat_keyboard(lang),
        parse_mode="HTML",
    )
    asyncio.create_task(_complete_search(message, state, lang))

async def _complete_search(message: Message, state: FSMContext, lang: str) -> None:
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
        tr(lang, "partner_found", name=partner["name"], age=partner["age"], gender=gender_label(partner["gender"], lang)),
        reply_markup=live_chat_keyboard(lang),
        parse_mode="HTML",
    )

@router.message(ChatStates.searching)
async def cancel_search(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if is_button(message.text, "end_chat"):
        await state.set_state(ChatStates.main_menu)
        await log_chat_event(message.from_user.id, message.from_user.username, "search_cancelled")
        await message.answer(tr(lang, "search_cancelled"), reply_markup=main_menu_keyboard(lang))
        return
    await message.answer(tr(lang, "search_wait"), reply_markup=live_chat_keyboard(lang))

@router.message(ChatStates.chat_18)
async def process_chat_18_message(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if is_button(message.text, "end_chat"):
        await state.clear()
        await state.set_state(ChatStates.main_menu)
        await log_chat_event(message.from_user.id, message.from_user.username, "chat_ended")
        await message.answer(tr(lang, "chat_session_ended"), reply_markup=main_menu_keyboard(lang))
        return

    if not await has_active_subscription(message.from_user.id):
        await state.set_state(ChatStates.main_menu)
        await message.answer(tr(lang, "sub_none"), reply_markup=buy_access_keyboard(_price_label(), lang))
        return

    data = await state.get_data()
    partner = data.get("virtual_partner") or {"name": "Partner", "age": 22, "gender": "ж", "opener": "Hi 🙂"}
    history = data.get("history_18", [])

    await log_chat_message(message.from_user.id, message.from_user.username, partner["name"], partner["age"], "user", message.text or "")
    await message.bot.send_chat_action(message.chat.id, "typing")
    reply = await get_virtual_reply(message.text or "", partner, history=history, lang=lang)

    history.append({"role": "user", "content": message.text or ""})
    history.append({"role": "assistant", "content": reply})
    if len(history) > MAX_HISTORY_PAIRS * 2:
        history = history[-(MAX_HISTORY_PAIRS * 2):]

    await state.update_data(history_18=history)
    await log_chat_message(message.from_user.id, message.from_user.username, partner["name"], partner["age"], "partner", reply)
    await message.answer(reply, reply_markup=live_chat_keyboard(lang))
