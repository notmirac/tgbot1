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

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Throttle на сообщения
    dp.message.middleware(ThrottleMiddleware())

    register_all_handlers(dp)

    # ИСПРАВЛЕНО: сначала удаляем вебхук явным запросом
    # потом дополнительно чистим очередь через getUpdates с offset
    await bot.delete_webhook(drop_pending_updates=True)

    # Дополнительная очистка накопившихся апдейтов
    # Это решает проблему зацикливания /start после перезапуска
    try:
        updates = await bot.get_updates(offset=-1, limit=1, timeout=1)
        if updates:
            await bot.get_updates(offset=updates[-1].update_id + 1, limit=1, timeout=1)
            logger.info("Очищено %d накопившихся апдейтов", len(updates))
    except Exception as e:
        logger.warning("Не удалось очистить апдейты: %s", e)

    logger.info("Бот запущен. Для остановки нажми Ctrl+C")
    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            # ИСПРАВЛЕНО: drop_pending_updates в polling тоже
            drop_pending_updates=True,
        )
    finally:
        await bot.session.close()
        logger.info("Бот остановлен.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Остановлен пользователем.")
