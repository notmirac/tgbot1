from __future__ import annotations

from typing import Any

SUPPORTED_LANGS = {"ru", "en"}
DEFAULT_LANG = "ru"

TEXTS: dict[str, dict[str, str]] = {
    "ru": {
        "btn_home": "🏠 Главное меню",
        "btn_profile": "👤 Моя анкета",
        "btn_chat": "💬 Чат",
        "btn_chat18": "🔞 Чат 18+",
        "btn_photo18": "🖼 Фото 18+",
        "btn_status": "💳 Подписка",
        "btn_language": "🌐 Язык",
        "btn_back": "◀️ Назад",
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
        "banned": "🚫 Вы заблокированы в боте.",
        "home": (
            "🏠 <b>Главное меню</b>\n\n"
            "• 👤 <b>Моя анкета</b>\n"
            "• 💬 <b>Чат</b>\n"
            "• 🔞 <b>Чат 18+</b>\n"
            "• 🖼 <b>Фото 18+</b>\n"
            "• 💳 <b>Подписка</b>\n"
            "• 🌐 <b>Язык</b>\n\nВыбирай 👇"
        ),
        "sub_active": "💳 <b>Подписка активна</b>\n📅 До: <b>{date}</b>",
        "sub_none": "💳 <b>Подписка не активна</b>\n\nОформи доступ ниже 👇",
        "lang_choose": "🌐 Выбери язык:",
        "lang_set": "✅ Язык изменён на Русский 🇷🇺",
        "lang_set_en": "✅ Language set to English 🇬🇧",
        "profile_required": "👤 Для этого нужна анкета. Нажми <b>👤 Моя анкета</b> и создай её.",
        "profile_none": "👤 <b>У тебя пока нет анкеты</b>\n\nВведи своё <b>имя</b>:",
        "profile_title": "👤 <b>Твоя анкета</b>",
        "profile_summary": "📝 Имя: <b>{name}</b>\n🎂 Возраст: <b>{age}</b>\n⚧ Пол: <b>{gender}</b>\n📋 Тип: <b>{ptype}</b>\n\nЧто хочешь изменить?",
        "profile_created": "✅ <b>Анкета создана!</b>\n\n📝 Имя: <b>{name}</b>\n🎂 Возраст: <b>{age}</b>\n⚧ Пол: <b>{gender}</b>{age_note}",
        "profile_recreated": "🔄 Анкета удалена. Создаём новую!\n\nВведи своё <b>имя</b>:",
        "profile_enter_name": "Введи своё <b>имя</b>:",
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
        "chat_enter": "💬 <b>Чат</b>\n\nПиши — я отвечу на выбранном языке. Для выхода нажми <b>◀️ Назад</b>.",
        "chat_reply_error": "Что-то пошло не так 😅 Попробуй ещё раз чуть позже.",
        "chat18_need_profile": "👤 Для раздела 18+ нужна анкета.",
        "chat18_underage": "🔞 Этот раздел только для совершеннолетних. Тебе {age} лет — доступ закрыт.",
        "chat18_need_sub": "🔒 Для чата 18+ нужна активная подписка.",
        "chat18_choose_gender": "🔞 Кого хочешь найти? Выбери пол:",
        "chat18_choose_age": "🔞 Выбери возраст собеседника:",
        "chat18_searching": "⏳ <b>Ищем собеседника…</b>\n\nСейчас онлайн: <b>~{size}</b>\nПодбираем анкету по твоим параметрам…",
        "chat18_gender_saved": "✅ Пол сохранён.",
        "chat18_age_invalid": "⚠️ Выбери возраст кнопкой ниже.",
        "search_already_chat": "❗ Ты уже в чате. Сначала заверши его.",
        "search_already_queue": "⏳ Ты уже в очереди поиска. Подожди немного.",
        "search_wait": "⏳ <b>Ищем собеседника…</b>\n\nВ очереди: <b>{size}</b>\n\nНажми «❌ Завершить чат», чтобы отменить поиск.",
        "search_wait_18": "⏳ <b>Ищем собеседника…</b>\n\nСейчас онлайн: <b>~{size}</b>\n\nНажми «❌ Завершить чат», чтобы отменить поиск.",
        "search_cancelled": "🔍 Поиск отменён.",
        "partner_found": "🎉 <b>Собеседник найден</b>\n\n{name}, {age} лет",
        "partner_found_fallback": "🎉 <b>Собеседник найден:</b> {name}",
        "chat_write_now": "Можешь начинать общение.",
        "chat_session_ended": "Пользователь завершил сеанс",
        "virtual_search_cancelled": "❌ Поиск отменён.",
        "chat_finished_self": "❌ Чат завершён.",
        "chat_finished_missing": "❌ Чат уже завершён.",
        "unsupported_message": "⚠️ Этот тип сообщений не поддерживается.",
        "subscription_info": "Подписка на {days} дней: Чат 18+ и Фото 18+ без ограничений.",
        "payments_unavailable": "⚠️ Платежи пока не настроены. Обратись к администратору.",
        "payment_title": "🔞 Доступ к 18+ контенту",
        "payment_description": "Полный доступ к разделам «Чат 18+» и «Фото 18+» на {days} дней.\n\n✅ Чат 18+\n✅ Фото 18+\n✅ Мгновенная активация",
        "payment_label": "Подписка на {days} дней",
        "payment_success": "🎉 <b>Оплата прошла успешно!</b>\n\n✅ Доступ активирован\n📅 Подписка действует до: <b>{date}</b>",
        "payment_failed_activation": "✅ Оплата прошла, но возникла ошибка при активации. Напиши администратору.",
        "photos_need_sub": "🖼 <b>Фото 18+</b>\n\n🔒 Этот раздел доступен только по подписке.",
        "photos_empty": "🖼 Фотографии пока не добавлены 😔",
        "photos_loading": "🖼 Загружаю для тебя…",
        "photos_done": "Это все фото 🌹",
        "admin_panel": "⚙️ <b>Админ-панель</b>",
        "admin_denied": "⛔ Нет доступа.",
        "admin_stats": "📊 <b>Статистика</b>\n\n👥 Пользователи: <b>{users}</b>\n👤 Анкеты: <b>{profiles}</b>\n🚫 Баны: <b>{banned}</b>\n💳 Активные подписки: <b>{subs}</b>",
        "admin_ban_list_empty": "Список банов пуст.",
    },
    "en": {
        "btn_home": "🏠 Main menu",
        "btn_profile": "👤 My Profile",
        "btn_chat": "💬 Chat",
        "btn_chat18": "🔞 Chat 18+",
        "btn_photo18": "🖼 Photos 18+",
        "btn_status": "💳 Subscription",
        "btn_language": "🌐 Language",
        "btn_back": "◀️ Back",
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
        "banned": "🚫 You are blocked in the bot.",
        "home": (
            "🏠 <b>Main menu</b>\n\n"
            "• 👤 <b>My Profile</b>\n"
            "• 💬 <b>Chat</b>\n"
            "• 🔞 <b>Chat 18+</b>\n"
            "• 🖼 <b>Photos 18+</b>\n"
            "• 💳 <b>Subscription</b>\n"
            "• 🌐 <b>Language</b>\n\nChoose 👇"
        ),
        "sub_active": "💳 <b>Subscription active</b>\n📅 Until: <b>{date}</b>",
        "sub_none": "💳 <b>No active subscription</b>\n\nBuy access below 👇",
        "lang_choose": "🌐 Choose language:",
        "lang_set": "✅ Language set to Russian 🇷🇺",
        "lang_set_en": "✅ Language set to English 🇬🇧",
        "profile_required": "👤 You need a profile for this. Tap <b>👤 My Profile</b> and create it.",
        "profile_none": "👤 <b>You don't have a profile yet</b>\n\nEnter your <b>name</b>:",
        "profile_title": "👤 <b>Your profile</b>",
        "profile_summary": "📝 Name: <b>{name}</b>\n🎂 Age: <b>{age}</b>\n⚧ Gender: <b>{gender}</b>\n📋 Type: <b>{ptype}</b>\n\nWhat would you like to change?",
        "profile_created": "✅ <b>Profile created!</b>\n\n📝 Name: <b>{name}</b>\n🎂 Age: <b>{age}</b>\n⚧ Gender: <b>{gender}</b>{age_note}",
        "profile_recreated": "🔄 Profile deleted. Let's create a new one!\n\nEnter your <b>name</b>:",
        "profile_enter_name": "Enter your <b>name</b>:",
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
        "chat_enter": "💬 <b>Chat</b>\n\nWrite something — I will reply in your selected language. Press <b>◀️ Back</b> to leave.",
        "chat_reply_error": "Something went wrong 😅 Please try again a bit later.",
        "chat18_need_profile": "👤 You need a profile for the 18+ section.",
        "chat18_underage": "🔞 This section is adults only. You are {age} years old — access denied.",
        "chat18_need_sub": "🔒 An active subscription is required for 18+ chat.",
        "chat18_choose_gender": "🔞 Who do you want to find? Choose gender:",
        "chat18_choose_age": "🔞 Choose partner age range:",
        "chat18_searching": "⏳ <b>Searching for a partner…</b>\n\nOnline now: <b>~{size}</b>\nMatching a profile to your preferences…",
        "chat18_gender_saved": "✅ Gender saved.",
        "chat18_age_invalid": "⚠️ Choose age using the buttons below.",
        "search_already_chat": "❗ You are already in a chat. End it first.",
        "search_already_queue": "⏳ You are already in the search queue. Please wait.",
        "search_wait": "⏳ <b>Searching for a partner…</b>\n\nIn queue: <b>{size}</b>\n\nPress “❌ End chat” to cancel.",
        "search_wait_18": "⏳ <b>Searching for a partner…</b>\n\nOnline now: <b>~{size}</b>\n\nPress “❌ End chat” to cancel.",
        "search_cancelled": "🔍 Search cancelled.",
        "partner_found": "🎉 <b>Partner found</b>\n\n{name}, {age} years old",
        "partner_found_fallback": "🎉 <b>Partner found:</b> {name}",
        "chat_write_now": "You can start chatting now.",
        "chat_session_ended": "User ended the session",
        "virtual_search_cancelled": "❌ Search cancelled.",
        "chat_finished_self": "❌ Chat finished.",
        "chat_finished_missing": "❌ The chat is already finished.",
        "unsupported_message": "⚠️ This message type is not supported.",
        "subscription_info": "Subscription for {days} days: Chat 18+ and Photos 18+ without limits.",
        "payments_unavailable": "⚠️ Payments are not configured yet. Contact the administrator.",
        "payment_title": "🔞 Access to 18+ content",
        "payment_description": "Full access to “Chat 18+” and “Photos 18+” for {days} days.\n\n✅ Chat 18+\n✅ Photos 18+\n✅ Instant activation",
        "payment_label": "Subscription for {days} days",
        "payment_success": "🎉 <b>Payment successful!</b>\n\n✅ Access activated\n📅 Subscription is valid until: <b>{date}</b>",
        "payment_failed_activation": "✅ Payment was successful, but activation failed. Please contact the administrator.",
        "photos_need_sub": "🖼 <b>Photos 18+</b>\n\n🔒 This section is available by subscription only.",
        "photos_empty": "🖼 No photos have been added yet 😔",
        "photos_loading": "🖼 Loading for you…",
        "photos_done": "That was all 🌹",
        "admin_panel": "⚙️ <b>Admin panel</b>",
        "admin_denied": "⛔ Access denied.",
        "admin_stats": "📊 <b>Statistics</b>\n\n👥 Users: <b>{users}</b>\n👤 Profiles: <b>{profiles}</b>\n🚫 Bans: <b>{banned}</b>\n💳 Active subscriptions: <b>{subs}</b>",
        "admin_ban_list_empty": "Ban list is empty.",
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
