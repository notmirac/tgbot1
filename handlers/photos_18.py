import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from config import config
from database import has_active_subscription
from keyboards import BTN_BACK, BTN_PHOTO18, buy_access_keyboard, main_menu_keyboard, live_chat_keyboard
from keyboards.photos_18 import photos_gender_kb, photos_nav_kb
from services.photo_profiles import ensure_photo_dirs, get_all_photos, make_profile_for_photo
from states import ChatStates, Photos18State

logger = logging.getLogger(__name__)
router = Router()
ensure_photo_dirs()


def _price_label() -> str:
    if config.currency == 'RUB':
        return f"{config.subscription_price // 100} руб."
    return f"{config.subscription_price / 100:.2f} {config.currency}"


def _caption(profile: dict) -> str:
    return (
        f"📋 {profile['name']}, {profile['age']} лет\n"
        f"Пол: {profile['gender_label']}\n\n"
        f"Хотите начать общение?"
    )


async def _send_current_photo(chat_target: Message, state: FSMContext) -> None:
    data = await state.get_data()
    gender = data.get('photos18_gender')
    index = int(data.get('photos18_index', 0))

    if gender not in {'male', 'female'}:
        await chat_target.answer('Сначала выбери раздел: мужские или женские фото.')
        return

    photos = get_all_photos(gender)
    if not photos:
        folder_name = 'photos_18/male' if gender == 'male' else 'photos_18/female'
        await chat_target.answer(
            f'📂 В папке {folder_name} пока нет фотографий.\n'
            f'Загрузи JPG/PNG/WEBP файлы и открой раздел снова.',
            reply_markup=main_menu_keyboard(),
        )
        return

    if index < 0:
        index = len(photos) - 1
    elif index >= len(photos):
        index = 0

    profile = make_profile_for_photo(gender, photos[index])
    await state.update_data(photos18_index=index, photos18_profile=profile)

    try:
        await chat_target.answer_photo(
            photo=FSInputFile(profile['photo_path']),
            caption=_caption(profile),
            reply_markup=photos_nav_kb(),
        )
    except Exception as exc:
        logger.exception('Ошибка отправки фото 18+: %s', exc)
        await chat_target.answer('⚠️ Не удалось открыть фотографию. Проверь файл и попробуй ещё раз.')


@router.message(lambda msg: msg.text == BTN_PHOTO18)
async def open_photos_18(message: Message, state: FSMContext) -> None:
    if not await has_active_subscription(message.from_user.id):
        await message.answer(
            '🖼 <b>Фотографии 18+</b>\n\n'
            '🔒 Этот раздел доступен только по подписке.\n\n'
            f'Стоимость: <b>{_price_label()}</b>',
            reply_markup=buy_access_keyboard(_price_label()),
            parse_mode='HTML',
        )
        return

    await state.clear()
    await state.set_state(Photos18State.choosing_gender)
    await state.update_data(photos18_gender=None, photos18_index=0, photos18_profile=None)
    await message.answer('Выбери, какие анкеты показать:', reply_markup=photos_gender_kb())


@router.message(Photos18State.choosing_gender)
async def choose_gender_by_text(message: Message, state: FSMContext) -> None:
    if message.text == BTN_BACK:
        await state.clear()
        await state.set_state(ChatStates.main_menu)
        await message.answer('Вернулся в меню 🏠', reply_markup=main_menu_keyboard())
        return
    await message.answer('Используй кнопки под сообщением, чтобы выбрать мужские или женские фото.')


@router.callback_query(F.data.startswith('photos18_gender:'))
async def choose_photos_gender(callback: CallbackQuery, state: FSMContext) -> None:
    gender = callback.data.split(':', 1)[1]
    if gender not in {'male', 'female'}:
        await callback.answer('Некорректный выбор', show_alert=True)
        return

    await state.set_state(Photos18State.browsing)
    await state.update_data(photos18_gender=gender, photos18_index=0, photos18_profile=None)
    await callback.answer()
    await _send_current_photo(callback.message, state)


@router.callback_query(F.data.startswith('photos18_nav:'))
async def navigate_photos(callback: CallbackQuery, state: FSMContext) -> None:
    action = callback.data.split(':', 1)[1]
    data = await state.get_data()
    index = int(data.get('photos18_index', 0))

    if action == 'prev':
        await state.update_data(photos18_index=index - 1)
        await callback.answer()
        await _send_current_photo(callback.message, state)
        return

    if action == 'next':
        await state.update_data(photos18_index=index + 1)
        await callback.answer()
        await _send_current_photo(callback.message, state)
        return

    if action == 'start':
        profile = data.get('photos18_profile')
        if not profile:
            await callback.answer('Сначала выбери анкету', show_alert=True)
            return

        await state.clear()
        await state.set_state(ChatStates.chat_18)
        await state.update_data(virtual_partner=profile, history_18=[])
        await callback.answer()
        await callback.message.answer(
            f"🎉 <b>Собеседник найден</b>\n\n{profile['name']}, {profile['age']} лет\n{profile['gender_label']}\n\nМожете начинать общение.",
            reply_markup=live_chat_keyboard(),
            parse_mode='HTML',
        )
        return

    await callback.answer('Неизвестное действие', show_alert=True)
