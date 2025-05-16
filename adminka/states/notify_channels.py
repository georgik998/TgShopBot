from aiogram.fsm.state import State, StatesGroup


class NotifyChannelEditStates(StatesGroup):
    new_channel_url = State()
