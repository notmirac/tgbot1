import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import config
from database import get_user_lang
from keyboards import main_menu_keyboard
from states import ChatStates
from utils.i18n import tr

logger = logging.getLogger(__name__)
router = Router()

OWNER_ALIASES = {"/owner", "owner"}

@router.message(Command("owner"))
async def owner_command(message: Message, state: FSMContext) -> None:
    if message.from_user.id != config.admin_id:
        return
    await state.clear()
    await state.set_state(ChatStates.main_menu)
    lang = await get_user_lang(message.from_user.id)
    await message.answer(
        tr(lang, "home"),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )

@router.message(lambda m: (m.text or "").strip().lower() in OWNER_ALIASES)
async def owner_text_command(message: Message, state: FSMContext) -> None:
    if message.from_user.id != config.admin_id:
        return
    await state.clear()
    await state.set_state(ChatStates.main_menu)
    lang = await get_user_lang(message.from_user.id)
    await message.answer(
        tr(lang, "home"),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )
