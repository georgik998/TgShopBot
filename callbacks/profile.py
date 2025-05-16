from aiogram.filters.callback_data import CallbackData


class PurchaseHistoryCallback(CallbackData, prefix='purchases-history'):
    page: int = 0


class PurchaseCallback(CallbackData, prefix='purchases-history-purchase'):
    id: str
    page: int


class ActivatePromocodeCallback(CallbackData, prefix='payment/promocode'):
    ...


class ReferralSystemCallback(CallbackData, prefix='profile/ref-system'):
    ...


class WithdrawReferralBalanceCallback(CallbackData, prefix='profile/ref-system/withdrawal'):
    ...


class GetPurchaseCallback(CallbackData, prefix='profile/purchases-history/get'):
    id: str
    page:int


