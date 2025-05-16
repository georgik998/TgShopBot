from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tg_bot.adminka.keyboards.main import back_to_admin_button, back_to_admin_kb

from tg_bot.adminka.callbacks.content import *
from tg_bot.adminka.callbacks.main import ContentCallback
from tg_bot.config import back_button_style

back_to_content_button = InlineKeyboardButton(text=back_button_style, callback_data=ContentCallback().pack())

select_content_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📝 Текста', callback_data=TextEditCallback().pack()),
            InlineKeyboardButton(text='🖼 Баннеры', callback_data=BannerEditCallback().pack())
        ],
        [
            back_to_admin_button
        ]
    ]
)

select_banner_field = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='/start', callback_data=BannerFieldCallback(field='start').pack()),
            InlineKeyboardButton(text='/catalog', callback_data=BannerFieldCallback(field='catalog').pack()),
        ],
        [
            InlineKeyboardButton(text='/profile', callback_data=BannerFieldCallback(field='profile').pack()),
            InlineKeyboardButton(text='/info', callback_data=BannerFieldCallback(field='info').pack()),
        ],
        [
            InlineKeyboardButton(text='/payment', callback_data=BannerFieldCallback(field='payment').pack()),
        ],
        [
            back_to_content_button
        ]
    ]
)
back_to_select_banner_field_button = InlineKeyboardButton(text=back_button_style,
                                                          callback_data=BannerEditCallback().pack())
back_to_select_banner_field = InlineKeyboardMarkup(
    inline_keyboard=[
        [back_to_select_banner_field_button]
    ]
)

select_text_field = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='/start', callback_data=TextFieldCallback(field='start').pack()),
            InlineKeyboardButton(text='/info', callback_data=TextFieldCallback(field='info').pack()),
        ],
        [
            InlineKeyboardButton(text='/faq', callback_data=TextFieldCallback(field='faq').pack()),
            InlineKeyboardButton(text='/payment', callback_data=TextFieldCallback(field='payment').pack()),
        ],
        [
            back_to_content_button
        ]
    ]
)
back_to_select_text_field_button = InlineKeyboardButton(text=back_button_style,
                                                        callback_data=TextEditCallback().pack())
back_to_select_text_field = InlineKeyboardMarkup(
    inline_keyboard=[
        [back_to_select_text_field_button]
    ]
)
confirm_text_update = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data=TextFieldConfirmCallback(action=True).pack()),
            InlineKeyboardButton(text='Нет', callback_data=TextFieldConfirmCallback(action=False).pack()),
        ],
        [
            back_to_select_text_field_button
        ]
    ]
)

confirm_banner_update = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data=BannerFieldConfirmCallback(action=True).pack()),
            InlineKeyboardButton(text='Нет', callback_data=BannerFieldConfirmCallback(action=False).pack()),
        ],
        [
            back_to_select_banner_field_button
        ]
    ]
)
