from aiogram.fsm.state import State, StatesGroup


class ContactsStates(StatesGroup):
    edit_url = State()