# main.py
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from database import init_db
from handlers import register_all_handlers
from middlewares.throttle import ThrottleMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Запуск бота…")

    await init_db()
    logger.info("База данных готова")

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # MemoryStorage — состояния сбрасываются при перезапуске.
    # Это нормально: /start всегда восстанавливает состояние.
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Throttle только на сообщения — НЕ на callback_query
    # (callback_query уже защищены от дублей на уровне Telegram)
    dp.message.middleware(ThrottleMiddleware())

    register_all_handlers(dp)

    # Сбрасываем вебхук и пропускаем накопившиеся апдейты
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Бот запущен. Для остановки нажми Ctrl+C")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        logger.info("Бот остановлен.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Остановлен пользователем.")
