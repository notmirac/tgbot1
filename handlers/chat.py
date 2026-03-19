# handlers/chat.py — обычный AI-чат (бесплатный)
import logging
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import has_profile
from keyboards import BTN_BACK, BTN_CHAT, chat_keyboard, main_menu_keyboard
from services import get_ai_reply
from states import ChatStates

logger = logging.getLogger(__name__)
router = Router()
MAX_HISTORY_PAIRS = 10


@router.message(lambda msg: msg.text == BTN_CHAT)
async def enter_chat(message: Message, state: FSMContext) -> None:
    """Вход в чат — проверяем анкету."""
    if not await has_profile(message.from_user.id):
        await message.answer(
            "👤 Для чата нужна анкета!\n"
            "Нажми <b>👤 Моя анкета</b> чтобы создать её.",
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
        return

    await state.set_state(ChatStates.chat)
    await state.update_data(history=[])
    await message.answer(
        "💬 <b>Чат</b>\n\nПиши — отвечу! 😊\n"
        "Для выхода нажми <b>◀️ Назад в меню</b>.",
        reply_markup=chat_keyboard(),
        parse_mode="HTML",
    )


@router.message(ChatStates.chat)
async def process_chat_message(message: Message, state: FSMContext) -> None:
    if message.text == BTN_BACK:
        await state.set_state(ChatStates.main_menu)
        await message.answer("Вернулся в меню 🏠", reply_markup=main_menu_keyboard())
        return

    await message.bot.send_chat_action(message.chat.id, "typing")
    data = await state.get_data()
    history = data.get("history", [])

    reply = await get_ai_reply(message.text, mode="chat", history=history)

    history.append({"role": "user",      "content": message.text})
    history.append({"role": "assistant", "content": reply})
    if len(history) > MAX_HISTORY_PAIRS * 2:
        history = history[-(MAX_HISTORY_PAIRS * 2):]

    await state.update_data(history=history)
    await message.answer(reply, reply_markup=chat_keyboard())
