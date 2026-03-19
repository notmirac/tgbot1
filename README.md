# 🤖 Telegram AI-бот

Полноценный Telegram-бот с чатом через OpenAI API, FSM-состояниями и разделом 18+.

---

## 📁 Структура проекта

```
tgbot/
├── main.py                  # Точка входа, запуск polling
├── requirements.txt         # Зависимости Python
├── .env.example             # Пример файла с переменными окружения
├── .env                     # Твои токены (НЕ коммить в git!)
│
├── config/
│   ├── __init__.py
│   └── settings.py          # Чтение переменных окружения
│
├── states/
│   ├── __init__.py
│   └── chat_states.py       # FSM-состояния (main_menu / chat / chat_18)
│
├── keyboards/
│   ├── __init__.py
│   └── main_menu.py         # Reply-клавиатуры
│
├── services/
│   ├── __init__.py
│   └── ai_service.py        # Интеграция с OpenAI API
│
└── handlers/
    ├── __init__.py           # Регистрация роутеров
    ├── start.py              # /start и кнопка «Главная»
    ├── chat.py               # Обычный чат
    ├── chat_18.py            # Чат 18+
    └── photos_18.py          # Отправка фото 18+
```

---

## ⚙️ Установка и запуск

### 1. Клонируй / распакуй проект

```bash
cd tgbot
```

### 2. Создай виртуальное окружение (рекомендуется)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Установи зависимости

```bash
pip install -r requirements.txt
```

### 4. Создай файл `.env`

Скопируй `.env.example` в `.env`:

```bash
cp .env.example .env
```

Открой `.env` в любом редакторе и заполни:

```env
BOT_TOKEN=123456789:AABBCCDDEEFFaabbccddeeff  # токен от @BotFather
OPENAI_API_KEY=sk-...                           # ключ OpenAI
```

### 5. Запусти бота

```bash
python main.py
```

Бот начнёт работать. Нажми **Ctrl+C** для остановки.

---

## 🔑 Где взять токены

| Токен | Где получить |
|---|---|
| `BOT_TOKEN` | Telegram → [@BotFather](https://t.me/BotFather) → `/newbot` |
| `OPENAI_API_KEY` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |

### Альтернативные API (бесплатные / дешевле)

Если OpenAI дорог, можно использовать совместимые API:

- **OpenRouter** — `https://openrouter.ai/api/v1` (много бесплатных моделей)
- **Together AI** — `https://api.together.xyz/v1`
- **Groq** — `https://api.groq.com/openai/v1` (очень быстрый, есть бесплатный tier)

Укажи в `.env`:
```env
OPENAI_BASE_URL=https://api.groq.com/openai/v1
OPENAI_API_KEY=gsk_...         # ключ от Groq
CHAT_MODEL=llama-3.1-8b-instant
```

---

## 🖼 Добавить фотографии 18+

В `.env` укажи через запятую прямые URL или Telegram file_id:

```env
PHOTO_18_IDS=https://example.com/photo1.jpg,https://example.com/photo2.jpg
```

**Как получить Telegram file_id:**
1. Отправь фото боту [@getidsbot](https://t.me/getidsbot)
2. Скопируй `file_id` из ответа
3. Вставь в `PHOTO_18_IDS`

---

## 🗒 Логи

Бот пишет логи одновременно в консоль и в файл `bot.log`.

---

## 🚀 Production (сервер / VPS)

Для постоянной работы используй `systemd` или `screen`:

```bash
# screen
screen -S tgbot
python main.py
# Ctrl+A, D — свернуть

# или через pm2 (Node.js менеджер, работает и с Python)
pm2 start "python main.py" --name tgbot
```

Для хранения FSM-состояний между перезапусками замени `MemoryStorage` на Redis:

```bash
pip install aiogram-redis-storage
```

```python
# main.py
from aiogram_redis_storage import RedisStorage
storage = RedisStorage.from_url("")
```
