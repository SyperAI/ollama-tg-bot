from aiogram.fsm.state import StatesGroup, State


class ChatState(StatesGroup):
    WAITING_MESSAGE = State()
    WAITING_RESPONSE = State()

