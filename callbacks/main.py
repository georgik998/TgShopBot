from aiogram.filters.callback_data import CallbackData


class CatalogCallback(CallbackData, prefix='catalog'):
    ...


class ProfileCallback(CallbackData, prefix='profile'):
    ...


class PaymentCallback(CallbackData, prefix='payment'):
    ...


class InfoCallback(CallbackData, prefix='info'):
    ...


class FaqCallback(CallbackData, prefix='faq'):
    ...


class FaqAnswerCallback(CallbackData, prefix='faq-answer'):
    id: int


class CheckSubscribe(CallbackData, prefix='check-subscribe'):
    ...
