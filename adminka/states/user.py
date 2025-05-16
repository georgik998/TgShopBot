from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    id = State()
    give_balance = State()
    claim_balance = State()
    send_sms = State()
    send_sms_confirm = State()
