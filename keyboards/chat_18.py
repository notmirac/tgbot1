# handlers/chat_18.py
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
    BTN_AGE_18_25, BTN_AGE_26_30, BTN_AGE_31_35,
    BTN_AGE_36_40, BTN_AGE_41_45, BTN_AGE_46_50,
    age_range_keyboard, buy_access_keyboard,
    gender_keyboard, live_chat_keyboard, main_menu_keyboard,
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
    lang    = await get_user_lang(user_id)

    try:
        profile = await get_profile(user_id)
    except Exception as e:
        logger.error("get_profile error user=%d: %s", user_id, e)
        await message.answer("⚠️ Ошибка. Попробуй ещё раз.", reply_markup=main_menu_keyboard(lang))
        return

    if not profile:
        await message.answer(tr(lang, "chat18_need_profile"), reply_markup=main_menu_keyboard(lang))
        return

    if profile["age"] < 18:
        await message.answer(tr(lang, "chat18_underage", age=profile["age"]), reply_markup=main_menu_keyboard(lang))
        return

    try:
        has_sub = await has_active_subscription(user_id)
    except Exception as e:
        logger.error("has_active_subscription error user=%d: %s", user_id, e)
        has_sub = False

    if not has_sub:
        await message.answer(
            tr(lang, "chat18_need_sub", price=_price_label()),
            reply_markup=buy_access_keyboard(_price_label(), lang),
            parse_mode="HTML",
        )
        return

    await state.clear()
    await state.set_state(ChatStates.waiting_partner_gender)

    try:
        prefs = await get_partner_preferences(user_id)
        hint  = gender_label(prefs["preferred_gender"], lang)
    except Exception:
        hint = gender_label("ж", lang)

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

    age_min, age_max     = AGE_RANGES[message.text]
    data                 = await state.get_data()
    preferred_gender     = data.get("preferred_gender", "ж")

    try:
        await set_partner_preferences(message.from_user.id, preferred_gender, age_min, age_max)
    except Exception as e:
        logger.error("set_partner_preferences error: %s", e)

    await state.update_data(preferred_age_min=age_min, preferred_age_max=age_max, history_18=[])
    await state.set_state(ChatStates.searching)

    approx_queue = random.randint(243, 267)

    try:
        await log_chat_event(
            message.from_user.id, message.from_user.username,
            "search_started", f"gender={preferred_gender} age={age_min}-{age_max}",
        )
    except Exception:
        pass

    await message.answer(
        tr(lang, "chat18_searching", size=approx_queue),
        reply_markup=live_chat_keyboard(lang),
        parse_mode="HTML",
    )

    # ИСПРАВЛЕНО: используем asyncio.ensure_future вместо create_task
    # и передаём user_id явно чтобы избежать race condition с message объектом
    asyncio.ensure_future(
        _complete_search(
            bot=message.bot,
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            state=state,
            lang=lang,
        )
    )


async def _complete_search(
    bot,
    chat_id: int,
    user_id: int,
    username: str | None,
    state: FSMContext,
    lang: str,
) -> None:
    """
    ИСПРАВЛЕНО:
    - принимаем bot, chat_id, user_id явно — не держим ссылку на message
    - проверяем состояние через ChatStates.searching (объект, не строка)
    - обёрнуто в try/except чтобы не падало молча
    """
    try:
        await asyncio.sleep(random.uniform(5.0, 6.0))

        # Проверяем что пользователь всё ещё в поиске
        current = await state.get_state()
        if current != ChatStates.searching:
            return

        data             = await state.get_data()
        preferred_gender = data.get("preferred_gender", "ж")
        age_min          = data.get("preferred_age_min", 18)
        age_max          = data.get("preferred_age_max", 25)

        partner = build_virtual_profile(
            preferred_gender=preferred_gender,
            age_min=age_min,
            age_max=age_max,
            lang=lang,
        )

        await state.update_data(virtual_partner=partner, history_18=[])
        await state.set_state(ChatStates.chat_18)

        try:
            await log_chat_event(
                user_id, username, "partner_found",
                f"{partner['name']} {partner['age']} {partner['gender']}",
            )
        except Exception:
            pass

        from keyboards import live_chat_keyboard
        await bot.send_message(
            chat_id,
            tr(lang, "partner_found",
               name=partner["name"],
               age=partner["age"],
               gender=gender_label(partner["gender"], lang)),
            reply_markup=live_chat_keyboard(lang),
            parse_mode="HTML",
        )

    except Exception as e:
        logger.error("_complete_search error user=%d: %s", user_id, e)
        try:
            from keyboards import main_menu_keyboard
            await bot.send_message(
                chat_id,
                "⚠️ Ошибка поиска. Попробуй ещё раз." if lang == "ru" else "⚠️ Search error. Try again.",
                reply_markup=main_menu_keyboard(lang),
            )
        except Exception:
            pass
        await state.set_state(ChatStates.main_menu)


@router.message(ChatStates.searching)
async def cancel_search(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if is_button(message.text, "end_chat"):
        await state.set_state(ChatStates.main_menu)
        try:
            await log_chat_event(message.from_user.id, message.from_user.username, "search_cancelled")
        except Exception:
            pass
        await message.answer(tr(lang, "search_cancelled"), reply_markup=main_menu_keyboard(lang))
        return
    await message.answer(tr(lang, "search_wait"), reply_markup=live_chat_keyboard(lang))


@router.message(ChatStates.chat_18)
async def process_chat_18_message(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)

    if is_button(message.text, "end_chat"):
        await state.clear()
        await state.set_state(ChatStates.main_menu)
        try:
            await log_chat_event(message.from_user.id, message.from_user.username, "chat_ended")
        except Exception:
            pass
        await message.answer(tr(lang, "chat_session_ended"), reply_markup=main_menu_keyboard(lang))
        return

    # Проверка подписки
    try:
        has_sub = await has_active_subscription(message.from_user.id)
    except Exception:
        has_sub = False

    if not has_sub:
        await state.set_state(ChatStates.main_menu)
        await message.answer(tr(lang, "sub_none"), reply_markup=buy_access_keyboard(_price_label(), lang))
        return

    data    = await state.get_data()
    partner = data.get("virtual_partner") or {
        "name": "Алина", "age": 22, "gender": "ж", "city": "", "interest": "", "lang": lang
    }
    history = data.get("history_18", [])

    # Показываем что печатаем
    try:
        await message.bot.send_chat_action(message.chat.id, "typing")
    except Exception:
        pass

    try:
        await log_chat_message(
            message.from_user.id, message.from_user.username,
            partner["name"], partner["age"], "user", message.text or "",
        )
    except Exception:
        pass

    # Получаем ответ AI
    try:
        reply = await get_virtual_reply(message.text or "", partner, history=history, lang=lang)
    except Exception as e:
        logger.error("get_virtual_reply error: %s", e)
        reply = "Прости, не расслышала." if lang == "ru" else "Sorry, missed that."

    # Обновляем историю
    history.append({"role": "user",      "content": message.text or ""})
    history.append({"role": "assistant", "content": reply})
    if len(history) > MAX_HISTORY_PAIRS * 2:
        history = history[-(MAX_HISTORY_PAIRS * 2):]

    await state.update_data(history_18=history)

    try:
        await log_chat_message(
            message.from_user.id, message.from_user.username,
            partner["name"], partner["age"], "partner", reply,
        )
    except Exception:
        pass

    await message.answer(reply, reply_markup=live_chat_keyboard(lang))
