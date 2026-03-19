# handlers/profile.py
import logging
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import get_profile, save_profile, delete_profile, has_profile
from keyboards import (
    BTN_PROFILE, BTN_BACK_PROFILE,
    BTN_MALE, BTN_FEMALE,
    BTN_EDIT_NAME, BTN_EDIT_AGE, BTN_EDIT_GENDER, BTN_RECREATE,
    gender_keyboard, profile_actions_keyboard, main_menu_keyboard,
)
from states import ProfileStates, EditProfileStates, ChatStates
from utils.profile_logger import log_profile

logger = logging.getLogger(__name__)
router = Router()
GENDERS = {BTN_MALE: "м", BTN_FEMALE: "ж"}
GENDER_LABELS = {"м": "👨 Мужской", "ж": "👩 Женский"}


@router.message(lambda msg: msg.text == BTN_PROFILE)
async def show_profile(message: Message, state: FSMContext) -> None:
    profile = await get_profile(message.from_user.id)
    if not profile:
        await state.set_state(ProfileStates.waiting_name)
        await message.answer(
            "👤 <b>У тебя пока нет анкеты</b>\n\nВведи своё <b>имя</b>:",
            reply_markup=main_menu_keyboard(), parse_mode="HTML",
        )
        return
    ptype  = "🔞 18+" if profile["profile_type"] == "adult" else "👤 Обычная"
    gender = GENDER_LABELS.get(profile["gender"], profile["gender"])
    await message.answer(
        f"👤 <b>Твоя анкета</b>\n\n"
        f"📝 Имя: <b>{profile['name']}</b>\n"
        f"🎂 Возраст: <b>{profile['age']}</b>\n"
        f"⚧ Пол: <b>{gender}</b>\n"
        f"📋 Тип: <b>{ptype}</b>\n\nЧто хочешь изменить?",
        reply_markup=profile_actions_keyboard(), parse_mode="HTML",
    )


@router.message(lambda msg: msg.text == BTN_BACK_PROFILE)
async def back_from_profile(message: Message, state: FSMContext) -> None:
    await state.set_state(ChatStates.main_menu)
    await message.answer("Вернулся в меню 🏠", reply_markup=main_menu_keyboard())


@router.message(ProfileStates.waiting_name)
async def process_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("⚠️ Имя слишком короткое:")
        return
    if len(name) > 30:
        await message.answer("⚠️ Имя слишком длинное (макс 30 символов):")
        return
    await state.update_data(name=name)
    await state.set_state(ProfileStates.waiting_age)
    await message.answer(
        f"Отлично, <b>{name}</b>! 👍\n\nВведи свой <b>возраст</b> (цифрами):",
        parse_mode="HTML",
    )


@router.message(ProfileStates.waiting_age)
async def process_age(message: Message, state: FSMContext) -> None:
    try:
        age = int(message.text.strip())
    except ValueError:
        await message.answer("⚠️ Введи возраст цифрами, например: <b>25</b>", parse_mode="HTML")
        return
    if age < 14:
        await message.answer("⚠️ Минимальный возраст — 14 лет.")
        return
    if age > 100:
        await message.answer("⚠️ Введи реальный возраст.")
        return
    await state.update_data(age=age)
    await state.set_state(ProfileStates.waiting_gender)
    await message.answer("Выбери свой <b>пол</b>:", reply_markup=gender_keyboard(), parse_mode="HTML")


@router.message(ProfileStates.waiting_gender)
async def process_gender(message: Message, state: FSMContext) -> None:
    if message.text not in GENDERS:
        await message.answer("⚠️ Нажми одну из кнопок:", reply_markup=gender_keyboard())
        return
    gender = GENDERS[message.text]
    data   = await state.get_data()
    name   = data["name"]
    age    = data["age"]
    profile_type = "adult" if age >= 18 else "normal"
    await save_profile(
        user_id=message.from_user.id,
        name=name, age=age, gender=gender, profile_type=profile_type,
    )
    log_profile(
        user_id=message.from_user.id,
        username=message.from_user.username,
        name=name, age=age, gender=gender, action="создана",
    )
    await state.set_state(ChatStates.main_menu)
    age_note = (
        "\n🔞 Тебе доступны разделы для взрослых (при наличии подписки)."
        if profile_type == "adult"
        else "\n👶 Разделы 18+ недоступны до 18 лет."
    )
    await message.answer(
        f"✅ <b>Анкета создана!</b>\n\n"
        f"📝 Имя: <b>{name}</b>\n"
        f"🎂 Возраст: <b>{age}</b>\n"
        f"⚧ Пол: <b>{message.text}</b>"
        f"{age_note}\n\nТеперь ты можешь пользоваться ботом! 🎉",
        reply_markup=main_menu_keyboard(), parse_mode="HTML",
    )


@router.message(lambda msg: msg.text == BTN_RECREATE)
async def recreate_profile(message: Message, state: FSMContext) -> None:
    await delete_profile(message.from_user.id)
    await state.set_state(ProfileStates.waiting_name)
    await message.answer(
        "🔄 Анкета удалена. Создаём новую!\n\nВведи своё <b>имя</b>:",
        reply_markup=main_menu_keyboard(), parse_mode="HTML",
    )


@router.message(lambda msg: msg.text == BTN_EDIT_NAME)
async def edit_name(message: Message, state: FSMContext) -> None:
    await state.set_state(EditProfileStates.editing_name)
    await message.answer("✏️ Введи новое имя:")


@router.message(EditProfileStates.editing_name)
async def save_new_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip()
    if len(name) < 2 or len(name) > 30:
        await message.answer("⚠️ Имя должно быть от 2 до 30 символов:")
        return
    profile = await get_profile(message.from_user.id)
    if profile:
        await save_profile(message.from_user.id, name, profile["age"], profile["gender"], profile["profile_type"])
    await state.set_state(ChatStates.main_menu)
    await message.answer(f"✅ Имя изменено на <b>{name}</b>", reply_markup=main_menu_keyboard(), parse_mode="HTML")


@router.message(lambda msg: msg.text == BTN_EDIT_AGE)
async def edit_age(message: Message, state: FSMContext) -> None:
    await state.set_state(EditProfileStates.editing_age)
    await message.answer("✏️ Введи новый возраст:")


@router.message(EditProfileStates.editing_age)
async def save_new_age(message: Message, state: FSMContext) -> None:
    try:
        age = int(message.text.strip())
    except ValueError:
        await message.answer("⚠️ Введи цифрами:")
        return
    if age < 14 or age > 100:
        await message.answer("⚠️ Введи реальный возраст (14–100):")
        return
    profile = await get_profile(message.from_user.id)
    if profile:
        profile_type = "adult" if age >= 18 else "normal"
        await save_profile(message.from_user.id, profile["name"], age, profile["gender"], profile_type)
    await state.set_state(ChatStates.main_menu)
    await message.answer(f"✅ Возраст изменён на <b>{age}</b>", reply_markup=main_menu_keyboard(), parse_mode="HTML")


@router.message(lambda msg: msg.text == BTN_EDIT_GENDER)
async def edit_gender(message: Message, state: FSMContext) -> None:
    await state.set_state(EditProfileStates.editing_gender)
    await message.answer("✏️ Выбери пол:", reply_markup=gender_keyboard())


@router.message(EditProfileStates.editing_gender)
async def save_new_gender(message: Message, state: FSMContext) -> None:
    if message.text not in GENDERS:
        await message.answer("⚠️ Нажми одну из кнопок:", reply_markup=gender_keyboard())
        return
    gender  = GENDERS[message.text]
    profile = await get_profile(message.from_user.id)
    if profile:
        await save_profile(message.from_user.id, profile["name"], profile["age"], gender, profile["profile_type"])
    await state.set_state(ChatStates.main_menu)
    await message.answer(f"✅ Пол изменён на <b>{message.text}</b>", reply_markup=main_menu_keyboard(), parse_mode="HTML")
