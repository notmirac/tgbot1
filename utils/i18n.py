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
        "btn_edit_name": "✏️ Изменить имя",
        "btn_edit_age": "✏️ Изменить возраст",
        "btn_edit_gender": "✏️ Изменить пол",
        "btn_recreate": "🔄 Пересоздать анкету",
        "btn_back_profile": "◀️ Назад",
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
        "profile_none": "👤 <b>У тебя пока нет анкеты</b>\n\nВведи своё <b>имя</b>:",
        "profile_title": "👤 <b>Твоя анкета</b>",
        "profile_summary": "📝 Имя: <b>{name}</b>\n🎂 Возраст: <b>{age}</b>\n⚧ Пол: <b>{gender}</b>\n📋 Тип: <b>{ptype}</b>\n\nЧто хочешь изменить?",
        "profile_created": "✅ <b>Анкета создана!</b>\n\n📝 Имя: <b>{name}</b>\n🎂 Возраст: <b>{age}</b>\n⚧ Пол: <b>{gender}</b>{age_note}\n\nТеперь ты можешь пользоваться ботом! 🎉",
        "profile_recreated": "🔄 Анкета удалена. Создаём новую!\n\nВведи своё <b>имя</b>:",
        "profile_name_short": "⚠️ Имя слишком короткое.",
        "profile_name_long": "⚠️ Имя слишком длинное. Максимум 30 символов.",
        "profile_enter_age": "Отлично, <b>{name}</b>! 👍\n\nВведи свой <b>возраст</b> цифрами:",
        "profile_age_digits": "⚠️ Введи возраст цифрами, например: <b>25</b>",
        "profile_age_min": "⚠️ Минимальный возраст — 14 лет.",
        "profile_age_max": "⚠️ Введи реальный возраст.",
        "profile_choose_gender": "Выбери свой <b>пол</b>:",
        "profile_gender_invalid": "⚠️ Нажми одну из кнопок ниже.",
        "profile_age_note_adult": "\n🔞 Тебе доступны разделы 18+ при активной подписке.",
        "profile_age_note_minor": "\n👶 Разделы 18+ недоступны до 18 лет.",
        "back_to_menu": "Вернулся в меню 🏠",
        "edit_name_prompt": "✏️ Введи новое имя:",
        "edit_age_prompt": "✏️ Введи новый возраст:",
        "edit_gender_prompt": "✏️ Выбери пол:",
        "edit_name_ok": "✅ Имя изменено на <b>{value}</b>",
        "edit_age_ok": "✅ Возраст изменён на <b>{value}</b>",
        "edit_gender_ok": "✅ Пол изменён на <b>{value}</b>",
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
        "support_intro": "📞 <b>Связь с администрацией</b>\n\n⏰ Время работы: <b>10:00–23:00</b>\n\nНапиши сообщение одним текстом, и мы передадим его администратору.",
        "support_sent": "✅ Сообщение отправлено администрации.",
        "support_empty": "⚠️ Напиши сообщение текстом.",
        "support_admin_message": "📩 <b>Новое обращение</b>\n\n👤 Пользователь: {name}\n🆔 ID: <code>{user_id}</code>\n🔗 Username: @{username}\n🌐 Язык: {lang}\n\n💬 Сообщение:\n{text}",
        "buy_access": "💳 Купить доступ — {price}",
        "subscription_more": "ℹ️ Что входит?",
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
        "btn_edit_name": "✏️ Edit name",
        "btn_edit_age": "✏️ Edit age",
        "btn_edit_gender": "✏️ Edit gender",
        "btn_recreate": "🔄 Recreate profile",
        "btn_back_profile": "◀️ Back",
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
        "profile_none": "👤 <b>You don't have a profile yet</b>\n\nEnter your <b>name</b>:",
        "profile_title": "👤 <b>Your profile</b>",
        "profile_summary": "📝 Name: <b>{name}</b>\n🎂 Age: <b>{age}</b>\n⚧ Gender: <b>{gender}</b>\n📋 Type: <b>{ptype}</b>\n\nWhat would you like to change?",
        "profile_created": "✅ <b>Profile created!</b>\n\n📝 Name: <b>{name}</b>\n🎂 Age: <b>{age}</b>\n⚧ Gender: <b>{gender}</b>{age_note}\n\nNow you can use the bot! 🎉",
        "profile_recreated": "🔄 Profile deleted. Let's create a new one!\n\nEnter your <b>name</b>:",
        "profile_name_short": "⚠️ Name is too short.",
        "profile_name_long": "⚠️ Name is too long. Maximum 30 characters.",
        "profile_enter_age": "Great, <b>{name}</b>! 👍\n\nEnter your <b>age</b> in digits:",
        "profile_age_digits": "⚠️ Enter age in digits, for example: <b>25</b>",
        "profile_age_min": "⚠️ Minimum age is 14.",
        "profile_age_max": "⚠️ Enter a realistic age.",
        "profile_choose_gender": "Choose your <b>gender</b>:",
        "profile_gender_invalid": "⚠️ Please tap one of the buttons below.",
        "profile_age_note_adult": "\n🔞 18+ sections are available with an active subscription.",
        "profile_age_note_minor": "\n👶 18+ sections are unavailable until you are 18.",
        "back_to_menu": "Back to main menu 🏠",
        "edit_name_prompt": "✏️ Enter a new name:",
        "edit_age_prompt": "✏️ Enter a new age:",
        "edit_gender_prompt": "✏️ Choose gender:",
        "edit_name_ok": "✅ Name changed to <b>{value}</b>",
        "edit_age_ok": "✅ Age changed to <b>{value}</b>",
        "edit_gender_ok": "✅ Gender changed to <b>{value}</b>",
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
        "support_intro": "📞 <b>Contact administration</b>\n\n⏰ Working hours: <b>10:00–23:00</b>\n\nSend one text message and we will forward it to the administrator.",
        "support_sent": "✅ Message sent to the administration.",
        "support_empty": "⚠️ Please send a text message.",
        "support_admin_message": "📩 <b>New support message</b>\n\n👤 User: {name}\n🆔 ID: <code>{user_id}</code>\n🔗 Username: @{username}\n🌐 Language: {lang}\n\n💬 Message:\n{text}",
        "buy_access": "💳 Buy access — {price}",
        "subscription_more": "ℹ️ What's included?",
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

def profile_type_label(profile_type: str | None, lang: str | None) -> str:
    lang = normalize_lang(lang)
    if profile_type == "adult":
        return "🔞 18+"
    return "👤 Обычная" if lang == "ru" else "👤 Regular"
