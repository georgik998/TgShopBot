from aiogram.fsm.state import State, StatesGroup


class FaqStates(StatesGroup):
    new_question = State()
    new_answer = State()
