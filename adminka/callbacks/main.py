from aiogram.filters.callback_data import CallbackData

base_prefix = 'adminka'


class AdminPanelCallback(CallbackData, prefix=base_prefix):
    ...


class StatisticCallback(CallbackData, prefix=base_prefix + 'statistic'):
    ...


class CatalogCallback(CallbackData, prefix=base_prefix + 'catalog'):
    ...


class SubscribeChannelsCallback(CallbackData, prefix=base_prefix + 'subscribe-channels'):
    ...


class NotifyChannelsCallback(CallbackData, prefix=base_prefix + 'notify-channels'):
    ...


class ContentCallback(CallbackData, prefix=base_prefix + 'content'):
    ...


class SpamCallback(CallbackData, prefix=base_prefix + 'spam'):
    ...


class PromocodeCallback(CallbackData, prefix=base_prefix + 'promocode'):
    ...


class PaymentCallback(CallbackData, prefix=base_prefix + 'payment'):
    ...


class UserCallback(CallbackData, prefix=base_prefix + 'user'):
    ...


class AdminCallback(CallbackData, prefix=base_prefix + 'admin'):
    ...


class FaqCallback(CallbackData, prefix=base_prefix + 'faq'):
    ...


class ContactCallback(CallbackData, prefix=base_prefix + 'contact'):
    ...


class RefLinksCallback(CallbackData, prefix=base_prefix + 'ref_links'):
    ...
