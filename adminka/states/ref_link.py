from aiogram.fsm.state import State, StatesGroup


class EditRefLink(StatesGroup):
    label = State()
