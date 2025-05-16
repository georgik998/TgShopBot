from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton
from typing import List, Sequence, Optional
from math import ceil

from tg_bot.infra.database.models import UserPurchases
from tg_bot.callbacks.main import *
from tg_bot.callbacks.profile import *
from tg_bot.callbacks.main import ProfileCallback, CatalogCallback

from tg_bot.config import back_button_style, pagination_next_page_style, pagination_previous_page_style, \
    pagination_last_page_style, pagination_first_page_style, element_on_page_in_profile_purchases


def build_profile():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🛍️ Мои заказы ', callback_data=PurchaseHistoryCallback().pack()),
                InlineKeyboardButton(text='📥 Пополнить', callback_data=PaymentCallback().pack())
            ],
            [
                InlineKeyboardButton(text='👥 Реф. Программа', callback_data=ReferralSystemCallback().pack()),
                InlineKeyboardButton(text='🎟️ Промокод', callback_data=ActivatePromocodeCallback().pack())
            ],
            # [
            #     InlineKeyboardButton(text=back_button_style, callback_data='/start'),
            # ]
        ]
    )


back_to_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=back_button_style, callback_data=ProfileCallback().pack())
        ]
    ]
)


def build_back_to_profile(style: Optional[str] = back_to_profile):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=style, callback_data=ProfileCallback().pack())
            ]
        ]
    )


def build_purchases(purchases: Sequence[UserPurchases], page):
    items_on_page = element_on_page_in_profile_purchases
    total_pages = ceil(len(purchases) / items_on_page) - 1
    kb = []
    for item in purchases[items_on_page * page:items_on_page * (page + 1)]:
        kb.append([
            InlineKeyboardButton(
                text=f'{item.name}',
                callback_data=PurchaseCallback(id=item.id, page=page).pack())
        ])
    if page == 0 == total_pages:
        # kb.append([InlineKeyboardButton(text='1/1', callback_data='snus')])
        ...
    elif page == 0:
        kb.append([
            # InlineKeyboardButton(text=f'1/{total_pages + 1}', callback_data='snus'),
            InlineKeyboardButton(text=pagination_next_page_style,
                                 callback_data=PurchaseHistoryCallback(page=page + 1).pack()),
            InlineKeyboardButton(text=pagination_last_page_style,
                                 callback_data=PurchaseHistoryCallback(page=total_pages).pack())

        ])
    elif total_pages == page:
        kb.append([
            InlineKeyboardButton(text=pagination_first_page_style,
                                 callback_data=PurchaseHistoryCallback(page=0).pack()),
            InlineKeyboardButton(text=pagination_previous_page_style,
                                 callback_data=PurchaseHistoryCallback(page=page - 1).pack()),
            # InlineKeyboardButton(text=f'{page + 1}/{total_pages + 1}', callback_data='snus'),
        ])
    else:
        kb.append([
            InlineKeyboardButton(text=pagination_first_page_style,
                                 callback_data=PurchaseHistoryCallback(page=0).pack()),
            InlineKeyboardButton(text=pagination_previous_page_style,
                                 callback_data=PurchaseHistoryCallback(page=page - 1).pack()),
            # InlineKeyboardButton(text=f'{page + 1}/{total_pages + 1}', callback_data='snus'),
            InlineKeyboardButton(text=pagination_next_page_style,
                                 callback_data=PurchaseHistoryCallback(page=page + 1).pack()),
            InlineKeyboardButton(text=pagination_last_page_style,
                                 callback_data=PurchaseHistoryCallback(page=total_pages).pack())
        ])
    kb.append([
        InlineKeyboardButton(text='‹ Вернуться в профиль', callback_data=ProfileCallback().pack())
    ])
    return InlineKeyboardMarkup(
        inline_keyboard=kb
    )


advise_to_make_first_purchases = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🛒 За покупками', callback_data=CatalogCallback().pack())
        ],
        [
            InlineKeyboardButton(text=back_button_style, callback_data=ProfileCallback().pack())
        ]
    ]
)


def purchase_view(page: int, purchase_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='📥 Получить товар',
                    callback_data=GetPurchaseCallback(page=page, id=purchase_id).pack()
                )
            ],
            # [
            #     InlineKeyboardButton(
            #         text='🆘 Помощь с товаром',
            #         callback_data=PurchaseHistoryCallback(page=page).pack()
            #     )
            # ],
            [
                InlineKeyboardButton(
                    text=back_button_style,
                    callback_data=PurchaseHistoryCallback(page=page).pack()
                )
            ]
        ]
    )


def get_purchase(purchase_id, page):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=back_button_style,
                    callback_data=PurchaseCallback(page=page, id=purchase_id).pack()
                )
            ]
        ]
    )


def ref_system_panel(url):
    share_text = f"""😍Смотри какого классного бота нашел! 
Здесь можно купить то что нам нужно!

🎁Все что нам нужно можно купить здесь! Заходи быстрее!
{url}"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(text='✔️ Скопировать реф. ссылку',
                                                     copy_text=CopyTextButton(text=share_text))
                            ],
                            [
                                InlineKeyboardButton(text='💸 Вывести на баланс',
                                                     callback_data=WithdrawReferralBalanceCallback().pack())
                            ],
                        ] + back_to_profile.inline_keyboard
    )


error_promo_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Перейти в каталог ›', callback_data=CatalogCallback().pack())
        ],
    ]
)
