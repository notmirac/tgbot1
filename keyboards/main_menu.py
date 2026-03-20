from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from utils.i18n import btn, tr

BTN_HOME = "🏠 Главное меню"
BTN_CHAT18 = "🔞 Чат 18+"
BTN_PHOTO18 = "🖼 Фотографии 18+"
BTN_BACK = "◀️ Назад в меню"
BTN_STATUS = "💳 Моя подписка"
BTN_PROFILE = "👤 Моя анкета"
BTN_END_CHAT = "❌ Завершить чат"
BTN_LANGUAGE = "🌐 Язык / Language"
BTN_SUPPORT = "📞 Связь с администрацией"
BTN_MALE = "👨 Мужской"
BTN_FEMALE = "👩 Женский"

BTN_AGE_18_25 = "18-25"
BTN_AGE_26_30 = "26-30"
BTN_AGE_31_35 = "31-35"
BTN_AGE_36_40 = "36-40"
BTN_AGE_41_45 = "41-45"
BTN_AGE_46_50 = "46-50"

BTN_EDIT_NAME = "✏️ Изменить имя"
BTN_EDIT_AGE = "✏️ Изменить возраст"
BTN_EDIT_GENDER = "✏️ Изменить пол"
BTN_RECREATE = "🔄 Пересоздать анкету"
BTN_BACK_PROFILE = "◀️ Назад"

def main_menu_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=btn(lang, "home")), KeyboardButton(text=btn(lang, "profile"))],
            [KeyboardButton(text=btn(lang, "chat18")), KeyboardButton(text=btn(lang, "photo18"))],
            [KeyboardButton(text=btn(lang, "status")), KeyboardButton(text=btn(lang, "language"))],
            [KeyboardButton(text=btn(lang, "support"))],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери раздел…" if lang == "ru" else "Choose a section…",
    )

def live_chat_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn(lang, "end_chat"))]],
        resize_keyboard=True,
    )

def gender_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=btn(lang, "male")), KeyboardButton(text=btn(lang, "female"))],
            [KeyboardButton(text=btn(lang, "back"))],
        ],
        resize_keyboard=True,
    )

def age_range_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_AGE_18_25), KeyboardButton(text=BTN_AGE_26_30)],
            [KeyboardButton(text=BTN_AGE_31_35), KeyboardButton(text=BTN_AGE_36_40)],
            [KeyboardButton(text=BTN_AGE_41_45), KeyboardButton(text=BTN_AGE_46_50)],
            [KeyboardButton(text=btn(lang, "back"))],
        ],
        resize_keyboard=True,
    )

def profile_actions_keyboard(lang: str = "ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=btn(lang, "edit_name")), KeyboardButton(text=btn(lang, "edit_age"))],
            [KeyboardButton(text=btn(lang, "edit_gender")), KeyboardButton(text=btn(lang, "recreate"))],
            [KeyboardButton(text=btn(lang, "back_profile"))],
        ],
        resize_keyboard=True,
    )

def buy_access_keyboard(price_label: str, lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=tr(lang, "buy_access", price=price_label), callback_data="buy_access")],
            [InlineKeyboardButton(text=tr(lang, "subscription_more"), callback_data="subscription_info")],
        ]
    )

def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
        ]]
    )
