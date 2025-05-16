from aiogram import F, Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from tg_bot.infra.database import async_session
from tg_bot.adminka.repositories.notify_channels import NotifyChannelRepo
from tg_bot.adminka.states.notify_channels import *

from tg_bot.adminka.callbacks.main import NotifyChannelsCallback
from tg_bot.adminka.callbacks.notify_channels import *
from tg_bot.adminka.keyboards import notify_channels as kb
from tg_bot.adminka.keyboards.main import back_to_admin_kb
from tg_bot.keyboards.main import cancel as cancel_kb

logs_names = {
    'payment': 'пополнений',
    'purchase': 'покупок',
    'promocode': 'промокодов',
    'new_user': 'новых пользователей'
}

router = Router()


@router.callback_query(NotifyChannelsCallback.filter(),
                       StateFilter(default_state, NotifyChannelEditStates.new_channel_url))
async def subscribe_channel_cmd(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        text='Ваши каналы для <b><i>логов</i></b>',
        reply_markup=kb.notify_channel_panel
    )

#
# @router.callback_query(DeleteNotifyChannelCallback.filter(), StateFilter(default_state))
# async def delete_notify_channel_cmd(call: CallbackQuery, callback_data: DeleteNotifyChannelCallback):
#     await call.message.edit_text(
#         f'Вы точно хотите отключить логи для <b>{logs_names[callback_data.channel]}</b> ?',
#         reply_markup=kb.build_confirm_delete(callback_data.channel)
#     )
#
#
# @router.callback_query(ConfirmDeleteNotifyChannelCallback.filter(), StateFilter(default_state))
# async def confirm_delete_channel_cmd(call: CallbackQuery, callback_data: ConfirmDeleteNotifyChannelCallback):
#     action = callback_data.action
#     channel = callback_data.channel
#     if action:
#         async with async_session() as session:
#             await NotifyChannelRepo(session).delete_channel(channel)
#         await call.message.edit_text(
#             f'Логи по <b>{logs_names[channel]}</b> отключены',
#             reply_markup=kb.back_to_notify_channels
#         )
#     else:
#         await call.message.edit_text(
#             f'Отменено',
#             reply_markup=kb.back_to_notify_channels
#         )


@router.callback_query(ChangeNotifyChannelCallback.filter(), StateFilter(default_state))
async def change_notify_channel_cmd(call: CallbackQuery, callback_data: ChangeNotifyChannelCallback, state: FSMContext):
    channel = callback_data.channel
    await state.set_state(NotifyChannelEditStates.new_channel_url)
    await state.update_data({'channel': channel})
    await call.message.edit_text(
        text=f"""Для того чтобы добавить канала для логов {logs_names[channel]}, выполните следующие действия
        
- Добавьте данного бота в группу и выдайте ему админ права

- Дождитесь пока бот пришлет id чата

- Пришлите сюда id чата""",
        reply_markup=kb.back_to_notify_channels
    )


@router.message(StateFilter(NotifyChannelEditStates.new_channel_url))
async def new_notify_channel_url_cmd(message: Message, state: FSMContext, bot: Bot):
    channel_id = message.text
    try:
        channel_id = int(channel_id)
    except Exception:
        await message.answer(
            'Ой-ой, видимо канала с такой ссылкой не существует или вы не назначили боту админ права в чате, попробуйте снова',
            reply_markup=kb.back_to_notify_channels
        )
        return
    channel = await state.get_value('channel')
    async with async_session() as session:
        await NotifyChannelRepo(session).add_channel(key=channel, channel_id=channel_id)
    await state.clear()
    await message.answer(
        'Канал для логов был успешно добавлен!',
        reply_markup=kb.back_to_notify_channels
    )
