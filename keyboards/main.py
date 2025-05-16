from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from typing import List
from tg_bot.infra.database.models import Faq
from tg_bot.callbacks.main import *

from tg_bot.config import back_button_style, cancel_button_style

# start = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text='🗂 Каталог товаров', callback_data=CatalogCallback().pack()),
#             InlineKeyboardButton(text='➕ Пополнить баланс', callback_data=PaymentCallback().pack())
#         ],
#         [
#             InlineKeyboardButton(text='🪪 Мой профиль', callback_data=ProfileCallback().pack()),
#             InlineKeyboardButton(text='ℹ️ Информация', callback_data=InfoCallback().pack())
#         ]
#     ]
# )

start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🗂 Каталог товаров'), KeyboardButton(text='➕ Пополнить баланс')],
        [KeyboardButton(text='🪪 Мой профиль'), KeyboardButton(text='ℹ️ Информация')]
    ],
    resize_keyboard=True
)
start_for_admin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🗂 Каталог товаров'), KeyboardButton(text='➕ Пополнить баланс')],
        [KeyboardButton(text='🪪 Мой профиль'), KeyboardButton(text='ℹ️ Информация')],
        [KeyboardButton(text='💠 Админ панель')]
    ],
    resize_keyboard=True
)

back_to_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=back_button_style, callback_data='/start')
        ]
    ]
)

cancel_button = InlineKeyboardButton(text=cancel_button_style, callback_data='cancel')
cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=cancel_button_style, callback_data='cancel')
        ]
    ]
)


def info(review_url, support_url, owner_url, news_url):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='👤 Поддержка', url=support_url),
                InlineKeyboardButton(text='👑 Владелец', url=owner_url)
            ],
            [
                InlineKeyboardButton(text='📖 Отзывы', url=review_url),
                InlineKeyboardButton(text='📰 Новости', url=news_url)
            ],
            [
                InlineKeyboardButton(text='❓ Часто задаваемые вопросы', callback_data=FaqCallback().pack())
            ],
            # [
            #     InlineKeyboardButton(text=back_button_style, callback_data='/start')
            # ]
        ]
    )


def build_faq(faq_info: List[Faq]):
    kb = []
    for faq in faq_info:
        kb.append([
            InlineKeyboardButton(text=faq.question, callback_data=FaqAnswerCallback(id=faq.id).pack())
        ])
    kb.append([
        InlineKeyboardButton(text=back_button_style, callback_data=InfoCallback().pack())
    ])
    return InlineKeyboardMarkup(
        inline_keyboard=kb
    )


back_to_faq = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=back_button_style, callback_data=FaqCallback().pack())
        ]
    ]
)


def channel_to_subscribe(channels_url):
    kb = []
    for i in range(0, len(channels_url), 2):
        layer = [InlineKeyboardButton(text=f'Канал №{i + 1}', url=channels_url[i])]
        try:
            layer.append(
                InlineKeyboardButton(text=f'Канал №{i + 2}', url=channels_url[i + 1])
            )
        except IndexError:
            pass
        kb.append(layer)
    kb.append([
        InlineKeyboardButton(text='✅Проверить', callback_data=CheckSubscribe().pack())
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)
