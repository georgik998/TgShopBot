from aiogram.filters.callback_data import CallbackData

from tg_bot.adminka.callbacks.main import base_prefix

prefix = base_prefix + 'user'


class BackToUserPanel(CallbackData, prefix=prefix + 'back'):
    id: int


class GiveBalanceUserCallbackData(CallbackData, prefix=prefix + 'give'):
    id: int


class ClaimBalanceUserCallbackData(CallbackData, prefix=prefix + 'claim'):
    id: int


class BanUserCallbackData(CallbackData, prefix=prefix + 'ban'):
    id: int


class UnbanUserCallbackData(CallbackData, prefix=prefix + 'unban'):
    id: int


class SendMessageUserCallbackData(CallbackData, prefix=prefix + 'send-message'):
    id: int


class SendMessageUserConfirmCallbackData(CallbackData, prefix= prefix + 'send-message/confirm'):
    action: bool
