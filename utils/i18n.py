from __future__ import annotations
from typing import Any

SUPPORTED_LANGS = {"ru", "en"}
DEFAULT_LANG = "ru"

TEXTS: dict[str, dict[str, str]] = {
    "ru": {
        "btn_home": "🏠 Главное меню",
        "btn_profile": "👤 Моя анкета",
        "btn_chat18": "🔞 Чат 18+",
        "btn_photo18": "🖼 Фотографии 18+",
        "btn_status": "💳 Моя подписка",
        "btn_language": "🌐 Язык / Language",
        "btn_support": "📞 Связь с администрацией",
        "btn_back": "◀️ Назад в меню",
        "btn_end_chat": "❌ Завершить чат",
        "btn_male": "👨 Мужской",
        "btn_female": "👩 Женский",
        "hello": "Привет, <b>{name}</b>! 👋\n\nВыбери раздел ниже:",
        "no_profile": "\n\n👤 Создай <b>анкету</b> — нажми «👤 Моя анкета».",
        "banned": "🚫 Ты заблокирован в боте.",
        "home": (
            "🏠 <b>Главная страница</b>\n\n"
            "• 👤 <b>Моя анкета</b>\n"
            "• 🔞 <b>Чат 18+</b>\n"
            "• 🖼 <b>Фотографии 18+</b>\n"
            "• 💳 <b>Моя подписка</b>\n"
            "• 🌐 <b>Язык</b>\n"
            "• 📞 <b>Связь с администрацией</b>\n\nВыбирай! 👇"
        ),
        "sub_active": "💳 <b>Подписка активна</b>\n📅 До: <b>{date}</b>\n\nВсе разделы доступны 🎉",
        "sub_none": "💳 <b>Нет подписки</b>\n\nКупи доступ 👇",
        "lang_choose": "🌐 Выбери язык:",
        "lang_set_ru": "✅ Язык изменён на Русский 🇷🇺",
        "lang_set_en": "✅ Language set to English 🇬🇧",
        "start_choose_lang": "🌐 Choose language / Выбери язык:",
        "chat18_need_profile": "👤 Для этого раздела нужна анкета.\nНажми «👤 Моя анкета», чтобы создать её.",
        "chat18_underage": "🔞 Этот раздел только для совершеннолетних.\nТебе {age} лет — доступ закрыт.",
        "chat18_need_sub": "🔞 <b>Чат 18+</b>\n\n🔒 Этот раздел доступен только по подписке.\n\nСтоимость: <b>{price}</b>",
        "chat18_choose_gender": "Кого ищем?",
        "chat18_current_gender": "Сейчас выбран: <b>{gender}</b>",
        "chat18_choose_age": "Выбери возраст собеседника:",
        "chat18_gender_invalid": "Выбери пол кнопкой ниже.",
        "chat18_age_invalid": "Выбери диапазон возраста кнопкой ниже.",
        "chat18_searching": "⏳ <b>Поиск собеседника...</b>\n\nВ очереди: примерно <b>{size}</b> человек\n\nСоединим автоматически через несколько секунд.",
        "search_cancelled": "Поиск остановлен.",
        "search_wait": "Ищем собеседника... Нажми «❌ Завершить чат», чтобы отменить.",
        "partner_found": "🎉 <b>Собеседник найден</b>\n\n{name}, {age} лет\n{gender}\n\nМожешь начинать общение.",
        "chat_session_ended": "Пользователь завершил сеанс",
        "buy_access": "💳 Купить доступ — {price}",
        "subscription_more": "ℹ️ Что входит?",
        "subscription_info": "Подписка на {days} дней.\n\n✅ Чат 18+\n✅ Фото 18+\n✅ Мгновенная активация",
        "support_intro": "📞 <b>Связь с администрацией</b>\n\n⏰ Время работы: <b>10:00–23:00</b>\n\nНапиши сообщение одним текстом, и мы передадим его администратору.",
        "support_sent": "✅ Сообщение отправлено администрации.",
        "support_empty": "⚠️ Напиши сообщение текстом.",
        "support_failed": "⚠️ Не удалось отправить сообщение администрации.",
        "support_admin_message": "📩 <b>Новое обращение</b>\n\n👤 Пользователь: {name}\n🆔 ID: <code>{user_id}</code>\n🔗 Username: @{username}\n🌐 Язык: {lang}\n\n💬 Сообщение:\n{text}",
    },
    "en": {
        "btn_home": "🏠 Main menu",
        "btn_profile": "👤 My Profile",
        "btn_chat18": "🔞 Chat 18+",
        "btn_photo18": "🖼 Photos 18+",
        "btn_status": "💳 My Subscription",
        "btn_language": "🌐 Language",
        "btn_support": "📞 Contact administration",
        "btn_back": "◀️ Back to menu",
        "btn_end_chat": "❌ End chat",
        "btn_male": "👨 Male",
        "btn_female": "👩 Female",
        "hello": "Hello, <b>{name}</b>! 👋\n\nChoose a section below:",
        "no_profile": "\n\n👤 Create a <b>profile</b> — tap «👤 My Profile».",
        "banned": "🚫 You are blocked.",
        "home": (
            "🏠 <b>Main menu</b>\n\n"
            "• 👤 <b>My Profile</b>\n"
            "• 🔞 <b>Chat 18+</b>\n"
            "• 🖼 <b>Photos 18+</b>\n"
            "• 💳 <b>My Subscription</b>\n"
            "• 🌐 <b>Language</b>\n"
            "• 📞 <b>Contact administration</b>\n\nChoose! 👇"
        ),
        "sub_active": "💳 <b>Subscription active</b>\n📅 Until: <b>{date}</b>\n\nAll sections are available 🎉",
        "sub_none": "💳 <b>No subscription</b>\n\nBuy access 👇",
        "lang_choose": "🌐 Choose language:",
        "lang_set_ru": "✅ Language set to Russian 🇷🇺",
        "lang_set_en": "✅ Language set to English 🇬🇧",
        "start_choose_lang": "🌐 Choose language / Выбери язык:",
        "chat18_need_profile": "👤 A profile is required for this section.\nTap “👤 My Profile” to create it.",
        "chat18_underage": "🔞 This section is for adults only.\nYou are {age} years old — access denied.",
        "chat18_need_sub": "🔞 <b>Chat 18+</b>\n\n🔒 This section is available only with a subscription.\n\nPrice: <b>{price}</b>",
        "chat18_choose_gender": "Who are we looking for?",
        "chat18_current_gender": "Currently selected: <b>{gender}</b>",
        "chat18_choose_age": "Choose the partner's age:",
        "chat18_gender_invalid": "Choose gender using the buttons below.",
        "chat18_age_invalid": "Choose an age range using the buttons below.",
        "chat18_searching": "⏳ <b>Searching for a partner...</b>\n\nIn queue: about <b>{size}</b> people\n\nYou will be connected automatically in a few seconds.",
        "search_cancelled": "Search stopped.",
        "search_wait": "Searching for a partner... Press “❌ End chat” to cancel.",
        "partner_found": "🎉 <b>Partner found</b>\n\n{name}, {age} years old\n{gender}\n\nYou can start chatting now.",
        "chat_session_ended": "User ended the session",
        "buy_access": "💳 Buy access — {price}",
        "subscription_more": "ℹ️ What's included?",
        "subscription_info": "Subscription for {days} days.\n\n✅ Chat 18+\n✅ Photos 18+\n✅ Instant activation",
        "support_intro": "📞 <b>Contact administration</b>\n\n⏰ Working hours: <b>10:00–23:00</b>\n\nSend one text message and we will forward it to the administrator.",
        "support_sent": "✅ Message sent to the administration.",
        "support_empty": "⚠️ Please send a text message.",
        "support_failed": "⚠️ Failed to send the message to administration.",
        "support_admin_message": "📩 <b>New support message</b>\n\n👤 User: {name}\n🆔 ID: <code>{user_id}</code>\n🔗 Username: @{username}\n🌐 Language: {lang}\n\n💬 Message:\n{text}",
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
        template = TEXTS[DEFAULT_LANG].get(key, key)
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
