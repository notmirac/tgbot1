from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def photos_gender_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='👨 Мужские', callback_data='photos18_gender:male')
    kb.button(text='👩 Женские', callback_data='photos18_gender:female')
    kb.adjust(2)
    return kb.as_markup()


def photos_nav_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='⬅️ Назад', callback_data='photos18_nav:prev')
    kb.button(text='➡️ Далее', callback_data='photos18_nav:next')
    kb.button(text='💬 Начать общение', callback_data='photos18_nav:start')
    kb.adjust(2, 1)
    return kb.as_markup()
