from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.adminka.callbacks.main import *
from tg_bot.config import back_button_style

admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📊 Статистика', callback_data=StatisticCallback().pack()),
            InlineKeyboardButton(text='🛒 Каталог', callback_data=CatalogCallback().pack())
        ],
        [
            InlineKeyboardButton(text='📌 Каналы для подписки', callback_data=SubscribeChannelsCallback().pack()),
            InlineKeyboardButton(text='📣 Каналы для логов', callback_data=NotifyChannelsCallback().pack())
        ],
        [
            InlineKeyboardButton(text='✏️ Текста/банеры', callback_data=ContentCallback().pack()),
            InlineKeyboardButton(text='💬 Рассылка', callback_data=SpamCallback().pack())
        ],
        [
            InlineKeyboardButton(text='👤 Пользователи', callback_data=UserCallback().pack()),
            InlineKeyboardButton(text='🔐 Управление админами', callback_data=AdminCallback().pack())
        ],
        [
            InlineKeyboardButton(text='🎟 Промокоды', callback_data=PromocodeCallback().pack()),
            InlineKeyboardButton(text='❓ FAQ', callback_data=FaqCallback().pack())
        ],
        [
            InlineKeyboardButton(text='📇 Ссылки на контакты', callback_data=ContactCallback().pack()),
            InlineKeyboardButton(text='🔗 Рекламные ссылки', callback_data=RefLinksCallback().pack()),
        ],
    ]
)

back_to_admin_button = InlineKeyboardButton(text=back_button_style, callback_data=AdminPanelCallback().pack())

back_to_admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            back_to_admin_button
        ]
    ]
)
