
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

BTN_HOME = "📌 Главная"
BTN_CHAT18 = "🔞 Чат 18+"
BTN_PHOTO18 = "🖼 Анкеты 18+"
BTN_BACK = "◀️ Назад в меню"
BTN_STATUS = "💳 Моя подписка"
BTN_PROFILE = "👤 Моя анкета"
BTN_END_CHAT = "❌ Завершить чат"
BTN_LANGUAGE = "🌐 Язык / Language"
BTN_SUPPORT = "📞 Связь с администрацией"
BTN_CHAT = "💬 Чат"
BTN_SEARCH = "🔍 Найти собеседника"
BTN_SEARCH18 = "🔞 Найти 18+"

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

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_HOME), KeyboardButton(text=BTN_PROFILE)],
            [KeyboardButton(text=BTN_CHAT18), KeyboardButton(text=BTN_PHOTO18)],
            [KeyboardButton(text=BTN_STATUS), KeyboardButton(text=BTN_LANGUAGE)],
            [KeyboardButton(text=BTN_SUPPORT)],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери раздел…",
    )

def chat_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=BTN_BACK)]], resize_keyboard=True)

def live_chat_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=BTN_END_CHAT)]], resize_keyboard=True)

def gender_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_MALE), KeyboardButton(text=BTN_FEMALE)], [KeyboardButton(text=BTN_BACK)]],
        resize_keyboard=True,
    )

def age_range_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_AGE_18_25), KeyboardButton(text=BTN_AGE_26_30)],
            [KeyboardButton(text=BTN_AGE_31_35), KeyboardButton(text=BTN_AGE_36_40)],
            [KeyboardButton(text=BTN_AGE_41_45), KeyboardButton(text=BTN_AGE_46_50)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )

def profile_actions_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_EDIT_NAME), KeyboardButton(text=BTN_EDIT_AGE)],
            [KeyboardButton(text=BTN_EDIT_GENDER), KeyboardButton(text=BTN_RECREATE)],
            [KeyboardButton(text=BTN_BACK_PROFILE)],
        ],
        resize_keyboard=True,
    )

def buy_access_keyboard(price_label: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Купить доступ — {price_label}", callback_data="buy_access")],
            [InlineKeyboardButton(text="ℹ️ Что входит?", callback_data="subscription_info")],
        ]
    )

def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"), InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]]
    )
