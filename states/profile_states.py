# states/profile_states.py
# ────────────────────────────────────────────────────────────
#  FSM-состояния для создания и редактирования анкеты.
# ────────────────────────────────────────────────────────────

from aiogram.fsm.state import State, StatesGroup


class ProfileStates(StatesGroup):
    """Пошаговое создание анкеты."""
    waiting_name   = State()   # шаг 1: ввод имени
    waiting_age    = State()   # шаг 2: ввод возраста
    waiting_gender = State()   # шаг 3: выбор пола


class EditProfileStates(StatesGroup):
    """Редактирование существующей анкеты."""
    choosing_field = State()   # выбор что редактировать
    editing_name   = State()   # редактирование имени
    editing_age    = State()   # редактирование возраста
    editing_gender = State()   # редактирование пола
