from aiogram.fsm.state import State, StatesGroup


class PromocodeStates(StatesGroup):
    new_name = State()
    new_quantity = State()
    new_content = State()
    new_type = State()
