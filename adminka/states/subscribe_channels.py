from aiogram.fsm.state import State, StatesGroup


class SubscribeChannelEditStates(StatesGroup):
    new_channel_url = State()
    new_channel_id = State()
