from aiogram.filters.callback_data import CallbackData

prefix = 'payment'


class PaymentAmountCallback(CallbackData, prefix=prefix + 'amount'):
    amount: float


class PaymentSystemCallback(CallbackData, prefix=prefix + 'system'):
    amount: float
    system: str







