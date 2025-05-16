from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.adminka.keyboards.main import back_to_admin_button
from tg_bot.adminka.callbacks.user import *
from tg_bot.adminka.callbacks.main import UserCallback
from tg_bot.config import back_button_style


def back_to_user_panel_button(user_id):
    return InlineKeyboardButton(text=back_button_style, callback_data=BackToUserPanel(id=user_id).pack())


def back_to_user_panel(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=back_button_style, callback_data=BackToUserPanel(id=user_id).pack())
            ]
        ]
    )


def user_manage_panel(user_id, ban):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Выдать баланс',
                                     callback_data=GiveBalanceUserCallbackData(id=user_id).pack()),
                InlineKeyboardButton(text='❌ Забрать баланс',
                                     callback_data=ClaimBalanceUserCallbackData(id=user_id).pack()),
            ],
            [
                InlineKeyboardButton(text='⛔️ Забанить', callback_data=BanUserCallbackData(
                    id=user_id).pack()) if not ban else InlineKeyboardButton(text='♻️ Разбанить',
                                                                             callback_data=UnbanUserCallbackData(
                                                                                 id=user_id).pack()),
                InlineKeyboardButton(text='💬 Отправить сообщение',
                                     callback_data=SendMessageUserCallbackData(id=user_id).pack()),
            ],
            [
                back_to_admin_button
            ]
        ]
    )


def confirm_send_sms(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Отправить',
                                     callback_data=SendMessageUserConfirmCallbackData(action=True).pack()),
                InlineKeyboardButton(text='❌ Отмена',
                                     callback_data=SendMessageUserConfirmCallbackData(action=False).pack()),

            ],
            [
                back_to_user_panel_button(user_id)
            ]
        ]
    )
