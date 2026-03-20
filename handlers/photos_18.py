from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import has_active_subscription, get_user_lang
from keyboards import buy_access_keyboard, main_menu_keyboard
from config import config
from utils.i18n import tr, is_button

router = Router()

def _price_label(lang: str) -> str:
    return f"{config.subscription_price_rub // 100} руб." if (lang or "ru") == "ru" else f"${config.subscription_price_usd / 100:.2f}"

@router.message(lambda msg: is_button(msg.text, "photo18"))
async def open_photos_18(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if not await has_active_subscription(message.from_user.id):
        title = "🖼 <b>Фотографии 18+</b>\n\n🔒 Этот раздел доступен только по подписке." if lang == "ru" else "🖼 <b>Photos 18+</b>\n\n🔒 This section is available only with a subscription."
        await message.answer(title + f"\n\n{'Стоимость' if lang == 'ru' else 'Price'}: <b>{_price_label(lang)}</b>", reply_markup=buy_access_keyboard(_price_label(lang), lang), parse_mode="HTML")
        return
    await message.answer("Раздел фото открыт." if lang == "ru" else "Photos section opened.", reply_markup=main_menu_keyboard(lang))
