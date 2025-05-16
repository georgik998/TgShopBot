from aiogram.filters.state import StatesGroup, State


class PromocodeStates(StatesGroup):
    promocode = State()
