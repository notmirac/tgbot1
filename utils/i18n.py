from __future__ import annotations
from typing import Any

SUPPORTED_LANGS = {"ru", "en"}
DEFAULT_LANG = "ru"

TEXTS: dict[str, dict[str, str]] = {
    "ru": {
        "btn_home": "📌 Главная",
        "btn_profile": "👤 Моя анкета",
        "btn_chat": "💬 Чат",
        "btn_chat18": "🔞 Чат 18+",
        "btn_photo18": "🖼 Анкеты 18+",
        "btn_status": "💳 Моя подписка",
        "btn_language": "🌐 Язык / Language",
        "btn_support": "📞 Связь с администрацией",
        "btn_back": "◀️ Назад в меню",
        "btn_end_chat": "❌ Завершить чат",
        "btn_male": "👨 Мужской",
        "btn_female": "👩 Женский",
        "btn_edit_name": "✏️ Изменить имя",
        "btn_edit_age": "✏️ Изменить возраст",
        "btn_edit_gender": "✏️ Изменить пол",
        "btn_recreate": "🔄 Пересоздать анкету",
        "btn_back_profile": "◀️ Назад",

        "home": (
            "📌 <b>Главная</b>\n\n"
            "• 👤 <b>Моя анкета</b>\n"
            "• 🔞 <b>Чат 18+</b>\n"
            "• 🖼 <b>Анкеты 18+</b>\n"
            "• 💳 <b>Моя подписка</b>\n"
            "• 🌐 <b>Язык</b>\n"
            "• 📞 <b>Связь с администрацией</b>\n\n"
            "Если бот завис или кнопки сломались — нажми <b>/start</b> или <b>/sstart</b>.\n\n"
            "Выбирай 👇"
        ),
        "hello": "Привет, <b>{name}</b>! 👋",
        "lang_choose": "🌐 Выбери язык:",
        "lang_set_ru": "✅ Язык изменён на Русский 🇷🇺",
        "lang_set_en": "✅ Language set to English 🇬🇧",
        "start_choose_lang": "🌐 Choose language / Выбери язык:",
        "banned": "🚫 Ты заблокирован в боте.",
        "sub_active": "💳 <b>Подписка активна</b>\n📅 До: <b>{date}</b>",
        "sub_none": "💳 <b>Нет подписки</b>\n\nКупи доступ 👇",
        "buy_access": "💳 Купить доступ — {price}",
        "subscription_more": "ℹ️ Что входит?",
        "support_intro": "📞 <b>Связь с администрацией</b>\n\n⏰ Время работы: <b>10:00–23:00</b>\n\nНапиши сообщение одним текстом, и мы передадим его администратору.",
        "support_sent": "✅ Сообщение отправлено администрации.",
        "support_empty": "⚠️ Напиши сообщение текстом.",
        "support_failed": "⚠️ Не удалось отправить сообщение администрации. Сначала открой бота с аккаунта администратора и нажми /start.",
        "back_to_menu": "Вернулся в меню 📌",
    },
    "en": {
        "btn_home": "📌 Main menu",
        "btn_profile": "👤 My Profile",
        "btn_chat": "💬 Chat",
        "btn_chat18": "🔞 Chat 18+",
        "btn_photo18": "🖼 Profiles 18+",
        "btn_status": "💳 My Subscription",
        "btn_language": "🌐 Language",
        "btn_support": "📞 Contact administration",
        "btn_back": "◀️ Back to menu",
        "btn_end_chat": "❌ End chat",
        "btn_male": "👨 Male",
        "btn_female": "👩 Female",
        "btn_edit_name": "✏️ Edit name",
        "btn_edit_age": "✏️ Edit age",
        "btn_edit_gender": "✏️ Edit gender",
        "btn_recreate": "🔄 Recreate profile",
        "btn_back_profile": "◀️ Back",

        "home": (
            "📌 <b>Main menu</b>\n\n"
            "• 👤 <b>My Profile</b>\n"
            "• 🔞 <b>Chat 18+</b>\n"
            "• 🖼 <b>Profiles 18+</b>\n"
            "• 💳 <b>My Subscription</b>\n"
            "• 🌐 <b>Language</b>\n"
            "• 📞 <b>Contact administration</b>\n\n"
            "If the bot freezes or the buttons stop working, send <b>/start</b> or <b>/sstart</b>.\n\n"
            "Choose 👇"
        ),
        "hello": "Hello, <b>{name}</b>! 👋",
        "lang_choose": "🌐 Choose language:",
        "lang_set_ru": "✅ Language set to Russian 🇷🇺",
        "lang_set_en": "✅ Language set to English 🇬🇧",
        "start_choose_lang": "🌐 Choose language / Выбери язык:",
        "banned": "🚫 You are blocked.",
        "sub_active": "💳 <b>Subscription active</b>\n📅 Until: <b>{date}</b>",
        "sub_none": "💳 <b>No subscription</b>\n\nBuy access 👇",
        "buy_access": "💳 Buy access — {price}",
        "subscription_more": "ℹ️ What's included?",
        "support_intro": "📞 <b>Contact administration</b>\n\n⏰ Working hours: <b>10:00–23:00</b>\n\nSend one text message and we will forward it to the administrator.",
        "support_sent": "✅ Message sent to the administration.",
        "support_empty": "⚠️ Please send a text message.",
        "support_failed": "⚠️ Failed to send the message to administration. First open the bot with the admin account and press /start.",
        "back_to_menu": "Back to main menu 📌",
    },
}

def normalize_lang(lang: str | None) -> str:
    if not lang:
        return DEFAULT_LANG
    lang = lang.lower()[:2]
    return lang if lang in SUPPORTED_LANGS else DEFAULT_LANG

def tr(lang: str | None, key: str, **kwargs: Any) -> str:
    lang = normalize_lang(lang)
    template = TEXTS.get(lang, TEXTS[DEFAULT_LANG]).get(key)
    if template is None:
        return key
    return template.format(**kwargs)

def btn(lang: str | None, key: str) -> str:
    return tr(lang, f"btn_{key}")

def is_button(text: str | None, key: str) -> bool:
    if not text:
        return False
    return text in {TEXTS["ru"].get(f"btn_{key}"), TEXTS["en"].get(f"btn_{key}")}

def gender_label(gender: str | None, lang: str | None) -> str:
    lang = normalize_lang(lang)
    if gender in {"м", "male"}:
        return btn(lang, "male")
    if gender in {"ж", "female"}:
        return btn(lang, "female")
    return gender or "—"

def profile_type_label(profile_type: str | None, lang: str | None) -> str:
    return "🔞 18+" if profile_type == "adult" else ("👤 Обычная" if normalize_lang(lang) == "ru" else "👤 Regular")
