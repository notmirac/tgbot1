import logging
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database import get_profile, save_profile, delete_profile, get_user_lang
from keyboards import gender_keyboard, profile_actions_keyboard, main_menu_keyboard
from states import ProfileStates, EditProfileStates, ChatStates
from utils.i18n import tr, is_button, gender_label, profile_type_label
from utils.profile_logger import log_profile

logger = logging.getLogger(__name__)
router = Router()

def _gender_value(text: str | None) -> str | None:
    if is_button(text, "male"):
        return "м"
    if is_button(text, "female"):
        return "ж"
    return None

async def _go_home(message: Message, state: FSMContext, lang: str) -> None:
    await state.clear()
    await state.set_state(ChatStates.main_menu)
    await message.answer(tr(lang, "back_to_menu"), reply_markup=main_menu_keyboard(lang))

def _is_leave_to_menu(text: str | None) -> bool:
    return (
        is_button(text, "home")
        or is_button(text, "back")
        or is_button(text, "back_profile")
    )

@router.message(lambda msg: is_button(msg.text, "profile"))
async def show_profile(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    profile = await get_profile(message.from_user.id)
    if not profile:
        await state.set_state(ProfileStates.waiting_name)
        await message.answer(
            tr(lang, "profile_none"),
            reply_markup=main_menu_keyboard(lang),
            parse_mode="HTML",
        )
        return

    await state.set_state(ChatStates.main_menu)
    await message.answer(
        f"{tr(lang, 'profile_title')}\n\n" +
        tr(
            lang,
            "profile_summary",
            name=profile["name"],
            age=profile["age"],
            gender=gender_label(profile["gender"], lang),
            ptype=profile_type_label(profile["profile_type"], lang),
        ),
        reply_markup=profile_actions_keyboard(lang),
        parse_mode="HTML",
    )

@router.message(lambda msg: is_button(msg.text, "back_profile"))
async def back_from_profile(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await _go_home(message, state, lang)

@router.message(ProfileStates.waiting_name)
async def process_name(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)

    if _is_leave_to_menu(message.text):
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
    await message.answer(tr(lang, "profile_enter_age", name=name), parse_mode="HTML")

@router.message(ProfileStates.waiting_age)
async def process_age(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)

    if _is_leave_to_menu(message.text):
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
        reply_markup=gender_keyboard(lang),
        parse_mode="HTML",
    )

@router.message(ProfileStates.waiting_gender)
async def process_gender(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)

    if _is_leave_to_menu(message.text):
        await _go_home(message, state, lang)
        return

    gender = _gender_value(message.text)
    if gender is None:
        await message.answer(tr(lang, "profile_gender_invalid"), reply_markup=gender_keyboard(lang))
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
        tr(
            lang,
            "profile_created",
            name=name,
            age=age,
            gender=gender_label(gender, lang),
            age_note=age_note,
        ),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )

@router.message(lambda msg: is_button(msg.text, "recreate"))
async def recreate_profile(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await delete_profile(message.from_user.id)
    await state.set_state(ProfileStates.waiting_name)
    await message.answer(
        tr(lang, "profile_recreated"),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )

@router.message(lambda msg: is_button(msg.text, "edit_name"))
async def edit_name(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await state.set_state(EditProfileStates.editing_name)
    await message.answer(tr(lang, "edit_name_prompt"))

@router.message(EditProfileStates.editing_name)
async def save_new_name(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)

    if _is_leave_to_menu(message.text):
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
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )

@router.message(lambda msg: is_button(msg.text, "edit_age"))
async def edit_age(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await state.set_state(EditProfileStates.editing_age)
    await message.answer(tr(lang, "edit_age_prompt"))

@router.message(EditProfileStates.editing_age)
async def save_new_age(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)

    if _is_leave_to_menu(message.text):
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
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )

@router.message(lambda msg: is_button(msg.text, "edit_gender"))
async def edit_gender(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)
    await state.set_state(EditProfileStates.editing_gender)
    await message.answer(tr(lang, "edit_gender_prompt"), reply_markup=gender_keyboard(lang))

@router.message(EditProfileStates.editing_gender)
async def save_new_gender(message: Message, state: FSMContext) -> None:
    lang = await get_user_lang(message.from_user.id)

    if _is_leave_to_menu(message.text):
        await _go_home(message, state, lang)
        return

    gender = _gender_value(message.text)
    if gender is None:
        await message.answer(tr(lang, "profile_gender_invalid"), reply_markup=gender_keyboard(lang))
        return

    profile = await get_profile(message.from_user.id)
    if profile:
        await save_profile(message.from_user.id, profile["name"], profile["age"], gender, profile["profile_type"])

    await state.clear()
    await state.set_state(ChatStates.main_menu)
    await message.answer(
        tr(lang, "edit_gender_ok", value=gender_label(gender, lang)),
        reply_markup=main_menu_keyboard(lang),
        parse_mode="HTML",
    )
