from aiogram.fsm.state import State, StatesGroup


class BuyProductStates(StatesGroup):
    promocode = State()
