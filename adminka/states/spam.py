from aiogram.filters.state import State, StatesGroup


class SpamStates(StatesGroup):
    sms = State()
    confirm = State()
