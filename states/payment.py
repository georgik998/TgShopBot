from aiogram.fsm.state import State, StatesGroup


class PaymentStates(StatesGroup):
    amount = State()


