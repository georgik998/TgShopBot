from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import StateFilter

from tg_bot.infra.database import async_session

from tg_bot.adminka.keyboards import faq as kb
from tg_bot.adminka.states.faq import *
from tg_bot.adminka.callbacks.faq import *
from tg_bot.adminka.repositories.faq import FaqRepo

from tg_bot.adminka.callbacks.main import FaqCallback
from tg_bot.adminka.keyboards.main import back_to_admin_kb

from tg_bot.adminka.utils import parse_text

router = Router()


@router.callback_query(
    FaqCallback.filter(),
    StateFilter(
        default_state,
        FaqStates.new_question
    ))
async def faq_panel_cmd(call: CallbackQuery, state: FSMContext):
    await state.clear()
    async with async_session() as session:
        faq_info = await FaqRepo(session).get_faq()
    await call.message.edit_text(
        text='Список вопросов faq, чтобы узнать ответ кликните на вопрос',
        reply_markup=kb.build_faq_panel(faq_info)
    )


@router.callback_query(FaqItemCallback.filter(), StateFilter(default_state))
async def faq_item_cmd(call: CallbackQuery, callback_data: FaqItemCallback):
    faq_id = callback_data.id
    async with async_session() as session:
        faq_info = await FaqRepo(session).get_faq_by_id(faq_id)
    await call.message.edit_text(
        text=faq_info.answer,
        reply_markup=kb.build_faq_item_panel(faq_id)
    )


@router.callback_query(DelFaqItemCallback.filter(), StateFilter(default_state))
async def del_faq_item_cmd(call: CallbackQuery, callback_data: DelFaqItemCallback):
    faq_id = callback_data.id
    await call.message.edit_text(
        'Вы точно хотите удалить вопрос?',
        reply_markup=kb.build_faq_item_del_confirm(faq_id)
    )


@router.callback_query(ConfirmDelFaqItemCallback.filter(), StateFilter(default_state))
async def confirm_del_faq_item_cmd(call: CallbackQuery, callback_data: ConfirmDelFaqItemCallback):
    faq_id = callback_data.id
    action = callback_data.action
    if not action:
        await call.message.edit_text(
            'Отменено',
            reply_markup=kb.back_to_faq_panel(faq_id)
        )
    else:
        async with async_session() as session:
            await FaqRepo(session).del_faq(question_id=faq_id)
        await call.message.edit_text(
            'Удалено',
            reply_markup=kb.back_to_faq
        )


@router.callback_query(NewFaqCallback.filter(), StateFilter(default_state))
async def new_faq_cmd(call: CallbackQuery, state: FSMContext):
    await state.set_state(FaqStates.new_question)
    await call.message.edit_text(
        'Пришлите вопрос для нового faq',
        reply_markup=kb.back_to_faq
    )


@router.message(StateFilter(FaqStates.new_question))
async def new_question_faq_cmd(message: Message, state: FSMContext):
    await state.update_data({
        'question': message.text
    })
    await state.set_state(FaqStates.new_answer)
    await message.answer(
        'Теперь пришлите ответ на вопрос для faq'
    )


@router.message(StateFilter(FaqStates.new_answer))
async def new_answer_faq_cmd(message: Message, state: FSMContext):
    answer = parse_text(message)
    question = await state.get_value('question')
    async with async_session() as session:
        await FaqRepo(session).add_faq(question=question, answer=answer)
    await state.clear()
    await message.answer(
        'Вопрос faq успешно добавлен',
        reply_markup=kb.back_to_faq
    )
