from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.exceptions import TelegramBadRequest

from tg_bot.adminka.callbacks.contact import *
from tg_bot.adminka.callbacks.main import ContactCallback
from tg_bot.adminka.states.contacts import *
from tg_bot.adminka.keyboards import contact as kb

from tg_bot.infra.database import async_session
from tg_bot.adminka.repositories.contact import ContactsRepo

router = Router()


@router.callback_query(
    ContactCallback.filter(),
    StateFilter(
        default_state,
        ContactsStates.edit_url
    )
)
async def contact_manage_cmd(call: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        contacts = await ContactsRepo(session).get_contacts()
    await state.clear()
    await call.message.edit_text(
        '<b><i>Текущие ссылки:</i></b>\n'
        f'Саппорт: {contacts.support}\n'
        f'Владелец: {contacts.owner}\n'
        f'Новости: {contacts.news}\n'
        f'Отзывы: {contacts.review}\n'
        f'\n'
        f'Выберите ссылку которую хотите изменить👇',
        reply_markup=kb.contact_manage,
        disable_web_page_preview=True
    )


@router.callback_query(EditContactCallback.filter(), StateFilter(default_state))
async def edit_contact_cmd(call: CallbackQuery, callback_data: EditContactCallback, state: FSMContext):
    contact = callback_data.contact
    await state.update_data({
        'contact': contact
    })
    await state.set_state(ContactsStates.edit_url)
    await call.message.edit_text(
        text='Пришлите новую ссылку',
        reply_markup=kb.back_to_contact_manage
    )


@router.message(StateFilter(ContactsStates.edit_url))
async def edit_contact_process_cmd(message: Message, state: FSMContext):
    try:
        await message.answer(
            'Новая ссылка успешно заменена',
            reply_markup=kb.test_url(message.text)
        )
        async with async_session() as session:
            await ContactsRepo(session).update(key=await state.get_value('contact'), value=message.text)
        await state.clear()
    except TelegramBadRequest:
        await message.answer(
            'Ссылка не рабочая, попробуйте снова',
            reply_markup=kb.back_to_contact_manage
        )
