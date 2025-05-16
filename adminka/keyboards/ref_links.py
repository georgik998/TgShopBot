from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.adminka.keyboards.main import back_to_admin_button
from tg_bot.config import back_button_style

from tg_bot.adminka.callbacks.ref_link import *
from tg_bot.adminka.callbacks.main import RefLinksCallback

from tg_bot.infra.database.models import RefLink
from typing import List

bact_to_ref_link_button = InlineKeyboardButton(text=back_button_style, callback_data=RefLinksCallback().pack())

bact_to_ref_link = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            bact_to_ref_link_button
        ]
    ]
)


def ref_links_manage_panel(links: List[RefLink]):
    kb = [
        [
            InlineKeyboardButton(
                text=link.id,
                callback_data=EditRefLinkCallback(id=link.id).pack()
            ),
            InlineKeyboardButton(
                text=f'{str(link.income).split(".")[0]}₽💸',
                callback_data=EditRefLinkCallback(id=link.id).pack()
            ),
            InlineKeyboardButton(
                text=f'{link.invited}👤',
                callback_data=EditRefLinkCallback(id=link.id).pack()
            ),
        ] for link in links
    ]
    kb += [
        [
            InlineKeyboardButton(text='➕ Новая ссылка', callback_data=NewRefLinkCallback().pack())
        ],
        [back_to_admin_button],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def edit_ref_link(ref_link: RefLink):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🌀 Сбросить статистику',
                    callback_data=ResetRefLinkCallback(id=ref_link.id).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text='✏️ Изменить метку',
                    callback_data=EditLabelRefLinKCallback(id=ref_link.id).pack()
                ),
                InlineKeyboardButton(
                    text='❌ Удалить',
                    callback_data=DelRefLinkCallback(id=ref_link.id).pack()
                )
            ],
            [
                bact_to_ref_link_button
            ]
        ]
    )


def back_to_edit_ref_link_button(id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=back_button_style, callback_data=EditRefLinkCallback(id=id).pack())
            ]
        ]
    )


def reset_ref_link_cmd(id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text='Да, я уверен',
                                    callback_data=ConfirmResetRefLinkCallback(id=id, action=True).pack()
                                ),
                                InlineKeyboardButton(
                                    text='❌ Нет, отменим',
                                    callback_data=ConfirmResetRefLinkCallback(id=id, action=False).pack()
                                ),
                            ],
                        ] + back_to_edit_ref_link_button(id).inline_keyboard
    )


def del_ref_link_cmd(id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text='Да, я уверен',
                                    callback_data=ConfirmDelRefLinkCallback(id=id, action=True).pack()
                                ),
                                InlineKeyboardButton(
                                    text='❌ Нет, отменим',
                                    callback_data=ConfirmDelRefLinkCallback(id=id, action=False).pack()
                                ),
                            ],
                        ] + back_to_edit_ref_link_button(id).inline_keyboard
    )
