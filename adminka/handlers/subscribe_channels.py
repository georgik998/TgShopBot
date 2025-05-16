from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from tg_bot.infra.database import async_session
from tg_bot.adminka.repositories.subscribe_channels import SubscribeChannelRepo
from tg_bot.adminka.states.subscribe_channels import *

from tg_bot.adminka.callbacks.main import SubscribeChannelsCallback
from tg_bot.adminka.callbacks.subscribe_channels import *
from tg_bot.adminka.keyboards import subscribe_channels as kb
from tg_bot.adminka.keyboards.main import back_to_admin_kb
from tg_bot.keyboards.main import cancel as cancel_kb

router = Router()


@router.callback_query(SubscribeChannelsCallback.filter(), StateFilter(default_state))
async def subscribe_channel_cmd(call: CallbackQuery):
    async with async_session() as session:
        channels = await SubscribeChannelRepo(session).get_channels()
    await call.message.edit_text(
        text='Ваши каналы на которые нужно обязательно подписаться',
        reply_markup=kb.build_subscribe_channel_panel(channels)
    )


@router.callback_query(SubscribeChannelNewCallback.filter(), StateFilter(default_state))
async def subscribe_channel_new_cmd(call: CallbackQuery, state: FSMContext):
    await state.set_state(SubscribeChannelEditStates.new_channel_id)
    await call.message.edit_text(
        text="""Для того чтобы добавить обязательную подписку на канал, выполните следующие действия
        
- Добавьте данного бота в канал и выдайте ему админ права
- Получить id канала от бота, и пришлите его сюда""",
        reply_markup=cancel_kb
    )


@router.message(StateFilter(SubscribeChannelEditStates.new_channel_id))
async def subscribe_channel_new_add_cmd(message: Message, state: FSMContext, bot):
    try:
        channel_id = int(message.text)
    except Exception:
        await message.answer(
            'ID должно быть целым числом, попробуйте снова',
            reply_markup=cancel_kb
        )
        return
    await state.update_data({'id': channel_id})
    await state.set_state(SubscribeChannelEditStates.new_channel_url)
    await message.answer(
        'Отлично, теперь пришлите ссылку на этот канал',
        reply_markup=cancel_kb
    )


@router.message(StateFilter(SubscribeChannelEditStates.new_channel_url))
async def new_channel_url(message: Message, state: FSMContext):
    channel_url = message.text
    channel_id = await state.get_value('id')
    await state.clear()
    async with async_session() as session:
        await SubscribeChannelRepo(session).add(channel_url, channel_id)
    await message.answer('Канал успешно добавлен!')


@router.callback_query(SubscribeChannelDeleteCallback.filter(), StateFilter(default_state))
async def delete_subscribe_channel_cmd(call: CallbackQuery, callback_data: SubscribeChannelDeleteCallback):
    channel_id = callback_data.id
    await call.message.edit_text(
        'Вы уверены что хотите удалить канал?',
        reply_markup=kb.build_confirm_delete_channel(channel_id)
    )


@router.callback_query(SubscribeChannelConfirmDeleteCallback.filter(), StateFilter(default_state))
async def delete_subscribe_channel_confirm_cmd(call: CallbackQuery,
                                               callback_data: SubscribeChannelConfirmDeleteCallback):
    channel_id = callback_data.id
    is_delete = callback_data.delete

    if is_delete:
        async with async_session() as session:
            await SubscribeChannelRepo(session).delete_channel(channel_id)
        await call.message.edit_text(
            'Канал успешно удален!',
            reply_markup=back_to_admin_kb
        )
    else:
        await call.message.edit_text(
            'Канал не был удален.',
            reply_markup=back_to_admin_kb
        )
