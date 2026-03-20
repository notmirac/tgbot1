import logging
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import get_profile, save_profile, delete_profile, get_user_lang
from keyboards import (
    BTN_PROFILE, BTN_BACK_PROFILE,
    BTN_MALE, BTN_FEMALE,
    BTN_EDIT_NAME, BTN_EDIT_AGE, BTN_EDIT_GENDER, BTN_RECREATE,
    BTN_HOME, BTN_STATUS, BTN_LANGUAGE, BTN_SUPPORT, BTN_CHAT18, BTN_PHOTO18, BTN_BACK,
    gender_keyboard, profile_actions_keyboard, main_menu_keyboard,
)
from states import ProfileStates, EditProfileStates, ChatStates
from utils.i18n import tr, gender_label, profile_type_label
from utils.profile_logger import log_profile

logger = logging.getLogger(__name__)
router = Router()

GENDERS = {
    BTN_MALE: "м",
    BTN_FEMALE: "ж",
    "👨 Male": "м",
    "👩 Female": "ж",
}

MENU_BUTTONS = {
    BTN_HOME, BTN_STATUS, BTN_LANGUAGE, BTN_SUPPORT, BTN_CHAT18, BTN_PHOTO18, BTN_BACK, BTN_BACK_PROFILE,
    "📌 Главная", "📌 Main menu",
    "💳 Моя подписка", "💳 My Subscription",
    "🌐 Язык / Language", "🌐 Language",
    "📞 Связь с администрацией", "📞 Contact administration",
    "🔞 Чат 18+", "🖼 Анкеты 18+", "🖼 Profiles 18+",
    "◀️ Назад в меню", "◀️ Back to menu", "◀️ Назад",
}

def _main_menu(lang: str):
    try:
        return main_menu_keyboard(lang)
    except TypeError:
        return main_menu_keyboard()

def _gender_kb(lang: str):
    try:
        return gender_keyboard(lang)
    except TypeError:
        return gender_keyboard()

def _profile_actions_kb(lang: str):
    try:
        return profile_actions_keyboard(lang)
    except TypeError:
        return profile_actions_keyboard()

async def _go_home(message: Message, state: FSMContext, lang: str) -> None:
    await state.clear()
    await state.set_state(ChatStates.main_menu)
    await message.answer(tr(lang, "back_to_menu"), reply_markup=_main_menu(lang))

def _wants_leave(text: str | None) -> bool:
    return (text or "").strip() in MENU_BUTTONS

@router.message(lambda msg: (msg.text or "").strip() in {BTN_PROFILE, "👤 My Profile"})
async def show_profile(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    profile = await get_profile(message.from_user.id)
    if not profile:
        await state.set_state(ProfileStates.waiting_name)
        await message.answer(
            tr(lang, "profile_none"),
            reply_markup=_main_menu(lang),
            parse_mode="HTML",
        )
        return

    ptype = profile_type_label(profile["profile_type"], lang)
    gender = gender_label(profile["gender"], lang)
    await state.set_state(ChatStates.main_menu)
    await message.answer(
        tr(lang, "profile_title") + "\n\n" +
        tr(lang, "profile_summary", name=profile["name"], age=profile["age"], gender=gender, ptype=ptype),
        reply_markup=_profile_actions_kb(lang), parse_mode="HTML",
    )

@router.message(lambda msg: (msg.text or "").strip() in {BTN_BACK_PROFILE, "◀️ Back"})
async def back_from_profile(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await _go_home(message, state, lang)

@router.message(ProfileStates.waiting_name)
async def process_name(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if _wants_leave(message.text):
        await _go_home(message, state, lang)
        return

    name = (message.text or "").strip()
    if len(name) < 2:
        await message.answer(tr(lang, "profile_name_short"))
        return
    if len(name) > 30:
        await message.answer(tr(lang, "profile_name_long"))
        return

    await state.update_data(name=name)
    await state.set_state(ProfileStates.waiting_age)
    await message.answer(
        tr(lang, "profile_enter_age", name=name),
        parse_mode="HTML",
    )

@router.message(ProfileStates.waiting_age)
async def process_age(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if _wants_leave(message.text):
        await _go_home(message, state, lang)
        return

    try:
        age = int((message.text or "").strip())
    except ValueError:
        await message.answer(tr(lang, "profile_age_digits"), parse_mode="HTML")
        return
    if age < 14:
        await message.answer(tr(lang, "profile_age_min"))
        return
    if age > 100:
        await message.answer(tr(lang, "profile_age_max"))
        return

    await state.update_data(age=age)
    await state.set_state(ProfileStates.waiting_gender)
    await message.answer(
        tr(lang, "profile_choose_gender"),
        reply_markup=_gender_kb(lang),
        parse_mode="HTML",
    )

@router.message(ProfileStates.waiting_gender)
async def process_gender(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if _wants_leave(message.text):
        await _go_home(message, state, lang)
        return

    gender = GENDERS.get((message.text or "").strip())
    if not gender:
        await message.answer(tr(lang, "profile_gender_invalid"), reply_markup=_gender_kb(lang))
        return

    data = await state.get_data()
    name = data["name"]
    age = data["age"]
    profile_type = "adult" if age >= 18 else "normal"

    await save_profile(
        user_id=message.from_user.id,
        name=name,
        age=age,
        gender=gender,
        profile_type=profile_type,
    )

    log_profile(
        user_id=message.from_user.id,
        username=message.from_user.username,
        name=name,
        age=age,
        gender=gender,
        action="created" if lang == "en" else "создана",
    )

    await state.clear()
    await state.set_state(ChatStates.main_menu)
    age_note = tr(lang, "profile_age_note_adult") if profile_type == "adult" else tr(lang, "profile_age_note_minor")
    await message.answer(
        tr(lang, "profile_created", name=name, age=age, gender=gender_label(gender, lang), age_note=age_note),
        reply_markup=_main_menu(lang), parse_mode="HTML",
    )

@router.message(lambda msg: (msg.text or "").strip() in {BTN_RECREATE, "🔄 Recreate profile"})
async def recreate_profile(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await delete_profile(message.from_user.id)
    await state.set_state(ProfileStates.waiting_name)
    await message.answer(
        tr(lang, "profile_recreated"),
        reply_markup=_main_menu(lang), parse_mode="HTML",
    )

@router.message(lambda msg: (msg.text or "").strip() in {BTN_EDIT_NAME, "✏️ Edit name"})
async def edit_name(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await state.set_state(EditProfileStates.editing_name)
    await message.answer(tr(lang, "edit_name_prompt"))

@router.message(EditProfileStates.editing_name)
async def save_new_name(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if _wants_leave(message.text):
        await _go_home(message, state, lang)
        return

    name = (message.text or "").strip()
    if len(name) < 2:
        await message.answer(tr(lang, "profile_name_short"))
        return
    if len(name) > 30:
        await message.answer(tr(lang, "profile_name_long"))
        return

    profile = await get_profile(message.from_user.id)
    if profile:
        await save_profile(message.from_user.id, name, profile["age"], profile["gender"], profile["profile_type"])

    await state.clear()
    await state.set_state(ChatStates.main_menu)
    await message.answer(
        tr(lang, "edit_name_ok", value=name),
        reply_markup=_main_menu(lang), parse_mode="HTML",
    )

@router.message(lambda msg: (msg.text or "").strip() in {BTN_EDIT_AGE, "✏️ Edit age"})
async def edit_age(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await state.set_state(EditProfileStates.editing_age)
    await message.answer(tr(lang, "edit_age_prompt"))

@router.message(EditProfileStates.editing_age)
async def save_new_age(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if _wants_leave(message.text):
        await _go_home(message, state, lang)
        return

    try:
        age = int((message.text or "").strip())
    except ValueError:
        await message.answer(tr(lang, "profile_age_digits"))
        return
    if age < 14:
        await message.answer(tr(lang, "profile_age_min"))
        return
    if age > 100:
        await message.answer(tr(lang, "profile_age_max"))
        return

    profile = await get_profile(message.from_user.id)
    if profile:
        profile_type = "adult" if age >= 18 else "normal"
        await save_profile(message.from_user.id, profile["name"], age, profile["gender"], profile_type)

    await state.clear()
    await state.set_state(ChatStates.main_menu)
    await message.answer(
        tr(lang, "edit_age_ok", value=age),
        reply_markup=_main_menu(lang), parse_mode="HTML",
    )

@router.message(lambda msg: (msg.text or "").strip() in {BTN_EDIT_GENDER, "✏️ Edit gender"})
async def edit_gender(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await state.set_state(EditProfileStates.editing_gender)
    await message.answer(tr(lang, "edit_gender_prompt"), reply_markup=_gender_kb(lang))

@router.message(EditProfileStates.editing_gender)
async def save_new_gender(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    if _wants_leave(message.text):
        await _go_home(message, state, lang)
        return

    gender = GENDERS.get((message.text or "").strip())
    if not gender:
        await message.answer(tr(lang, "profile_gender_invalid"), reply_markup=_gender_kb(lang))
        return

    profile = await get_profile(message.from_user.id)
    if profile:
        await save_profile(message.from_user.id, profile["name"], profile["age"], gender, profile["profile_type"])

    await state.clear()
    await state.set_state(ChatStates.main_menu)
    await message.answer(
        tr(lang, "edit_gender_ok", value=gender_label(gender, lang)),
        reply_markup=_main_menu(lang), parse_mode="HTML",
    )
