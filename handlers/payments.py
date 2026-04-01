from aiogram import Router, F
from aiogram.types import CallbackQuery

from config import config
from database import get_user_lang
from utils.i18n import tr

router = Router()


@router.callback_query(F.data == "subscription_info")
async def subscription_info(callback: CallbackQuery):
    lang = await get_user_lang(callback.from_user.id)

    await callback.answer()
    await callback.message.answer(
        tr(lang, "subscription_info", days=config.subscription_days),
        parse_mode="HTML",
    )
