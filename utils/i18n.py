from __future__ import annotations
from typing import Any

SUPPORTED_LANGS = {"ru", "en"}
DEFAULT_LANG = "ru"

TEXTS: dict[str, dict[str, str]] = {
    "ru": {
        # ── Кнопки ────────────────────────────────────────────
        "btn_home":         "📌 Главная",
        "btn_profile":      "👤 Моя анкета",
        "btn_chat":         "💬 Чат",
        "btn_chat18":       "🔞 Чат 18+",
        "btn_photo18":      "🖼 Анкеты 18+",
        "btn_status":       "💳 Моя подписка",
        "btn_language":     "🌐 Язык / Language",
        "btn_support":      "📞 Связь с администрацией",
        "btn_back":         "◀️ Назад в меню",
        "btn_end_chat":     "❌ Завершить чат",
        "btn_male":         "👨 Мужской",
        "btn_female":       "👩 Женский",
        "btn_edit_name":    "✏️ Изменить имя",
        "btn_edit_age":     "✏️ Изменить возраст",
        "btn_edit_gender":  "✏️ Изменить пол",
        "btn_recreate":     "🔄 Пересоздать анкету",
        "btn_back_profile": "◀️ Назад",

        # ── Главная ────────────────────────────────────────────
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
        "hello":             "Привет, <b>{name}</b>! 👋",
        "back_to_menu":      "Вернулся в меню 📌",

        # ── Язык ───────────────────────────────────────────────
        "lang_choose":       "🌐 Выбери язык:",
        "lang_set_ru":       "✅ Язык изменён на Русский 🇷🇺",
        "lang_set_en":       "✅ Language set to English 🇬🇧",
        "start_choose_lang": "🌐 Choose language / Выбери язык:",

        # ── Системные ─────────────────────────────────────────
        "banned": "🚫 Ты заблокирован в боте.",

        # ── Подписка ───────────────────────────────────────────
        "sub_active":         "💳 <b>Подписка активна</b>\n📅 До: <b>{date}</b>",
        "sub_none":           "💳 <b>Нет подписки</b>\n\nКупи доступ 👇",
        "buy_access":         "💳 Купить доступ — {price}",
        "subscription_more":  "ℹ️ Что входит?",
        "subscription_info":  "✅ Чат 18+ и Анкеты 18+ на <b>{days} дней</b>.",

        # ── Поддержка ──────────────────────────────────────────
        "support_intro":   "📞 <b>Связь с администрацией</b>\n\n⏰ Время работы: <b>10:00–23:00</b>\n\nНапиши сообщение одним текстом.",
        "support_sent":    "✅ Сообщение отправлено администрации.",
        "support_empty":   "⚠️ Напиши сообщение текстом.",
        "support_failed":  "⚠️ Не удалось отправить. Попробуй позже.",

        # ── Анкета — просмотр ──────────────────────────────────
        "profile_none":    "👤 <b>У тебя пока нет анкеты</b>\n\nВведи своё <b>имя</b>:",
        "profile_title":   "👤 <b>Твоя анкета</b>",
        "profile_summary": "📝 Имя: <b>{name}</b>\n🎂 Возраст: <b>{age}</b>\n⚧ Пол: <b>{gender}</b>\n📋 Тип: <b>{ptype}</b>\n\nЧто хочешь изменить?",

        # ── Анкета — создание ──────────────────────────────────
        "profile_enter_age":     "Отлично, <b>{name}</b>! 👍\n\nВведи свой <b>возраст</b> (цифрами):",
        "profile_choose_gender": "Выбери свой <b>пол</b>:",
        "profile_name_short":    "⚠️ Имя слишком короткое. Введи нормальное имя:",
        "profile_name_long":     "⚠️ Имя слишком длинное (максимум 30 символов):",
        "profile_age_digits":    "⚠️ Введи возраст цифрами, например: <b>25</b>",
        "profile_age_min":       "⚠️ Минимальный возраст — 14 лет.",
        "profile_age_max":       "⚠️ Введи реальный возраст (до 100).",
        "profile_gender_invalid":"⚠️ Нажми одну из кнопок:",
        "profile_age_note_adult":"🔞 Тебе доступны разделы для взрослых (при наличии подписки).",
        "profile_age_note_minor":"👶 Разделы 18+ недоступны до 18 лет.",
        "profile_created": (
            "✅ <b>Анкета создана!</b>\n\n"
            "📝 Имя: <b>{name}</b>\n"
            "🎂 Возраст: <b>{age}</b>\n"
            "⚧ Пол: <b>{gender}</b>\n"
            "{age_note}\n\n"
            "Теперь ты можешь пользоваться ботом! 🎉"
        ),
        "profile_recreated": "🔄 Анкета удалена. Создаём новую!\n\nВведи своё <b>имя</b>:",

        # ── Анкета — редактирование ────────────────────────────
        "edit_name_prompt":   "✏️ Введи новое имя:",
        "edit_name_ok":       "✅ Имя изменено на <b>{value}</b>",
        "edit_age_prompt":    "✏️ Введи новый возраст:",
        "edit_age_ok":        "✅ Возраст изменён на <b>{value}</b>",
        "edit_gender_prompt": "✏️ Выбери пол:",
        "edit_gender_ok":     "✅ Пол изменён на <b>{value}</b>",

        # ── Чат 18+ ────────────────────────────────────────────
        "chat18_need_profile":    "👤 Для этого раздела нужна анкета!\nНажми <b>👤 Моя анкета</b>.",
        "chat18_underage":        "🔞 Этот раздел только для совершеннолетних.\nТебе {age} лет — доступ закрыт.",
        "chat18_need_sub":        "🔞 <b>Чат 18+</b>\n\n🔒 Только по подписке.\n\nСтоимость: <b>{price}</b>",
        "chat18_choose_gender":   "Кого ищешь? Выбери пол собеседника:",
        "chat18_current_gender":  "Сейчас выбрано: <b>{gender}</b>",
        "chat18_gender_invalid":  "⚠️ Нажми одну из кнопок:",
        "chat18_choose_age":      "Выбери возраст собеседника:",
        "chat18_age_invalid":     "⚠️ Выбери диапазон из кнопок:",
        "chat18_searching":       "🔍 <b>Ищем собеседника...</b>\n\nВ очереди: ~{size} чел.\n\nНажми ❌ чтобы отменить.",
        "partner_found":          "🎉 <b>Собеседник найден!</b>\n\n👤 {name}, {age} лет, {gender}\n\nМожешь писать! 😊",
        "search_cancelled":       "🔍 Поиск отменён.",
        "search_wait":            "⏳ Ищем собеседника... Нажми ❌ чтобы отменить.",
        "chat_session_ended":     "❌ <b>Чат завершён.</b>\n\nВозвращайся когда захочешь! 👋",
    },

    "en": {
        # ── Кнопки ────────────────────────────────────────────
        "btn_home":         "📌 Main menu",
        "btn_profile":      "👤 My Profile",
        "btn_chat":         "💬 Chat",
        "btn_chat18":       "🔞 Chat 18+",
        "btn_photo18":      "🖼 Profiles 18+",
        "btn_status":       "💳 My Subscription",
        "btn_language":     "🌐 Language",
        "btn_support":      "📞 Contact administration",
        "btn_back":         "◀️ Back to menu",
        "btn_end_chat":     "❌ End chat",
        "btn_male":         "👨 Male",
        "btn_female":       "👩 Female",
        "btn_edit_name":    "✏️ Edit name",
        "btn_edit_age":     "✏️ Edit age",
        "btn_edit_gender":  "✏️ Edit gender",
        "btn_recreate":     "🔄 Recreate profile",
        "btn_back_profile": "◀️ Back",

        # ── Главная ────────────────────────────────────────────
        "home": (
            "📌 <b>Main menu</b>\n\n"
            "• 👤 <b>My Profile</b>\n"
            "• 🔞 <b>Chat 18+</b>\n"
            "• 🖼 <b>Profiles 18+</b>\n"
            "• 💳 <b>My Subscription</b>\n"
            "• 🌐 <b>Language</b>\n"
            "• 📞 <b>Contact administration</b>\n\n"
            "If the bot freezes or buttons stop working, send <b>/start</b> or <b>/sstart</b>.\n\n"
            "Choose 👇"
        ),
        "hello":             "Hello, <b>{name}</b>! 👋",
        "back_to_menu":      "Back to main menu 📌",

        # ── Язык ───────────────────────────────────────────────
        "lang_choose":       "🌐 Choose language:",
        "lang_set_ru":       "✅ Language set to Russian 🇷🇺",
        "lang_set_en":       "✅ Language set to English 🇬🇧",
        "start_choose_lang": "🌐 Choose language / Выбери язык:",

        # ── Системные ─────────────────────────────────────────
        "banned": "🚫 You are blocked.",

        # ── Подписка ───────────────────────────────────────────
        "sub_active":         "💳 <b>Subscription active</b>\n📅 Until: <b>{date}</b>",
        "sub_none":           "💳 <b>No subscription</b>\n\nBuy access 👇",
        "buy_access":         "💳 Buy access — {price}",
        "subscription_more":  "ℹ️ What's included?",
        "subscription_info":  "✅ Chat 18+ and Profiles 18+ for <b>{days} days</b>.",

        # ── Поддержка ──────────────────────────────────────────
        "support_intro":   "📞 <b>Contact administration</b>\n\n⏰ Working hours: <b>10:00–23:00</b>\n\nSend one text message.",
        "support_sent":    "✅ Message sent to the administration.",
        "support_empty":   "⚠️ Please send a text message.",
        "support_failed":  "⚠️ Failed to send. Try again later.",

        # ── Анкета — просмотр ──────────────────────────────────
        "profile_none":    "👤 <b>You don't have a profile yet</b>\n\nEnter your <b>name</b>:",
        "profile_title":   "👤 <b>Your profile</b>",
        "profile_summary": "📝 Name: <b>{name}</b>\n🎂 Age: <b>{age}</b>\n⚧ Gender: <b>{gender}</b>\n📋 Type: <b>{ptype}</b>\n\nWhat would you like to change?",

        # ── Анкета — создание ──────────────────────────────────
        "profile_enter_age":     "Great, <b>{name}</b>! 👍\n\nEnter your <b>age</b> (numbers only):",
        "profile_choose_gender": "Choose your <b>gender</b>:",
        "profile_name_short":    "⚠️ Name is too short. Enter a real name:",
        "profile_name_long":     "⚠️ Name is too long (max 30 characters):",
        "profile_age_digits":    "⚠️ Enter age as a number, e.g. <b>25</b>",
        "profile_age_min":       "⚠️ Minimum age is 14.",
        "profile_age_max":       "⚠️ Enter a real age (up to 100).",
        "profile_gender_invalid":"⚠️ Tap one of the buttons:",
        "profile_age_note_adult":"🔞 Adult sections are available (with an active subscription).",
        "profile_age_note_minor":"👶 18+ sections are not available until age 18.",
        "profile_created": (
            "✅ <b>Profile created!</b>\n\n"
            "📝 Name: <b>{name}</b>\n"
            "🎂 Age: <b>{age}</b>\n"
            "⚧ Gender: <b>{gender}</b>\n"
            "{age_note}\n\n"
            "You can now use the bot! 🎉"
        ),
        "profile_recreated": "🔄 Profile deleted. Let's create a new one!\n\nEnter your <b>name</b>:",

        # ── Анкета — редактирование ────────────────────────────
        "edit_name_prompt":   "✏️ Enter a new name:",
        "edit_name_ok":       "✅ Name changed to <b>{value}</b>",
        "edit_age_prompt":    "✏️ Enter a new age:",
        "edit_age_ok":        "✅ Age changed to <b>{value}</b>",
        "edit_gender_prompt": "✏️ Choose gender:",
        "edit_gender_ok":     "✅ Gender changed to <b>{value}</b>",

        # ── Чат 18+ ────────────────────────────────────────────
        "chat18_need_profile":    "👤 You need a profile to use this section!\nTap <b>👤 My Profile</b>.",
        "chat18_underage":        "🔞 This section is for adults only.\nYou are {age} years old — access denied.",
        "chat18_need_sub":        "🔞 <b>Chat 18+</b>\n\n🔒 Subscription required.\n\nPrice: <b>{price}</b>",
        "chat18_choose_gender":   "Who are you looking for? Choose partner gender:",
        "chat18_current_gender":  "Currently selected: <b>{gender}</b>",
        "chat18_gender_invalid":  "⚠️ Tap one of the buttons:",
        "chat18_choose_age":      "Choose partner age range:",
        "chat18_age_invalid":     "⚠️ Choose a range from the buttons:",
        "chat18_searching":       "🔍 <b>Searching for a partner...</b>\n\nIn queue: ~{size} people\n\nTap ❌ to cancel.",
        "partner_found":          "🎉 <b>Partner found!</b>\n\n👤 {name}, {age} y.o., {gender}\n\nStart chatting! 😊",
        "search_cancelled":       "🔍 Search cancelled.",
        "search_wait":            "⏳ Searching... Tap ❌ to cancel.",
        "chat_session_ended":     "❌ <b>Chat ended.</b>\n\nCome back anytime! 👋",
    },
}


def normalize_lang(lang: str | None) -> str:
    if not lang:
        return DEFAULT_LANG
    lang = str(lang).lower()[:2]
    return lang if lang in SUPPORTED_LANGS else DEFAULT_LANG


def tr(lang: str | None, key: str, **kwargs: Any) -> str:
    """Получить переведённый текст по ключу. Никогда не возвращает голый ключ."""
    lang = normalize_lang(lang)
    template = TEXTS.get(lang, {}).get(key)
    if template is None:
        # Пробуем дефолтный язык
        template = TEXTS.get(DEFAULT_LANG, {}).get(key)
    if template is None:
        # Крайний случай — возвращаем ключ чтобы было видно что не хватает перевода
        return f"[{key}]"
    if kwargs:
        try:
            return template.format(**kwargs)
        except KeyError:
            return template
    return template


def btn(lang: str | None, key: str) -> str:
    """Получить текст кнопки."""
    return tr(lang, f"btn_{key}")


def is_button(text: str | None, key: str) -> bool:
    """Проверить что текст совпадает с кнопкой на любом языке."""
    if not text:
        return False
    text = text.strip()
    return text in {
        TEXTS["ru"].get(f"btn_{key}", ""),
        TEXTS["en"].get(f"btn_{key}", ""),
    }


def gender_label(gender: str | None, lang: str | None) -> str:
    lang = normalize_lang(lang)
    if gender in {"м", "male", "м".lower()}:
        return btn(lang, "male")
    if gender in {"ж", "female"}:
        return btn(lang, "female")
    return gender or "—"


def profile_type_label(profile_type: str | None, lang: str | None) -> str:
    if profile_type == "adult":
        return "🔞 18+"
    return "👤 Обычная" if normalize_lang(lang) == "ru" else "👤 Regular"
