from aiogram import Dispatcher
from . import chat, chat_18, photos_18, start, payments, profile, admin


def register_all_handlers(dp: Dispatcher):
    dp.include_router(admin.router)
    dp.include_router(payments.router)
    dp.include_router(profile.router)
    dp.include_router(start.router)
    dp.include_router(chat.router)
    dp.include_router(chat_18.router)
    dp.include_router(photos_18.router)
