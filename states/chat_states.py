# states/chat_states.py
from aiogram.fsm.state import State, StatesGroup

class ChatStates(StatesGroup):
    main_menu               = State()
    chat                    = State()
    waiting_partner_gender  = State()
    waiting_partner_age     = State()
    searching               = State()
    chat_18                 = State()
    in_chat                 = State()
    waiting_support_message = State()
    browsing_profiles       = State()  # листание анкет 18+
