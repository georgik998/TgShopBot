from aiogram.fsm.state import State, StatesGroup


class EditTextStates(StatesGroup):
    text = State()
    confirm = State()


class EditBannerStates(StatesGroup):
    banner = State()
    confirm = State()
