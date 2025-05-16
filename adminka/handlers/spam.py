from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from tg_bot.adminka.callbacks.main import SpamCallback
from tg_bot.adminka.states.spam import SpamStates
from tg_bot.adminka.keyboards.main import back_to_admin_kb
from tg_bot.adminka.keyboards import spam as kb
from tg_bot.adminka.callbacks.spam import *

from tg_bot.infra.database import async_session
from tg_bot.adminka.repositories.user import UserRepo

router = Router()


@router.callback_query(SpamCallback.filter(), StateFilter(default_state))
async def spam_cmd(call: CallbackQuery, state: FSMContext):
    await state.set_state(SpamStates.sms)
    await call.message.edit_text(
        'Отправьте сообщение которое хотите использовать для рассылки',
        reply_markup=back_to_admin_kb
    )


@router.message(StateFilter(SpamStates.sms))
async def spam_sms_cmd(message: Message, state: FSMContext, bot: Bot):
    await state.update_data({
        'message_id': message.message_id,
    })
    await state.set_state(SpamStates.confirm)
    await bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )
    await message.answer(
        'Проверьте сообщение сверху, если оно верно, переходим к следующему этапу',
        reply_markup=kb.confirm_sms
    )


@router.callback_query(ConfirmSmsCallback.filter(), StateFilter(SpamStates.confirm))
async def confirm_spam_sms_cmd(call: CallbackQuery, state: FSMContext, callback_data: ConfirmSmsCallback, bot: Bot):
    action = callback_data.action
    if not action:
        await state.clear()
        await call.message.edit_text(
            'Отменено',
            reply_markup=back_to_admin_kb
        )
    else:
        await call.answer('Начинаю рассылку...')
        message_id = await state.get_value('message_id')
        async with async_session() as session:
            users = await UserRepo(session).get_all()
        success_send = 0
        error_send = 0
        for user in users:
            try:
                await bot.copy_message(
                    chat_id=user.tg_id,
                    from_chat_id=call.message.chat.id,
                    message_id=message_id
                )
                success_send += 1
            except TelegramForbiddenError:
                error_send += 1
            except TelegramBadRequest:
                error_send += 1
        await state.clear()
        await call.message.edit_text(
            'Рассылка закончена\n'
            '\n'
            f'📩Всего отправок: <code>{success_send + error_send}</code>\n'
            f'✅Успешных отправок: <b>{success_send}</b>\n'
            f'❌Неуспешных отправок: <i>{error_send}</i>'
        )
