from aiogram.fsm.state import State, StatesGroup


class Photos18State(StatesGroup):
    choosing_gender = State()
    browsing = State()
