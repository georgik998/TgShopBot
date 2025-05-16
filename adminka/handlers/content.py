from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import StateFilter

from tg_bot.adminka.keyboards import content as kb
from tg_bot.adminka.states.content import *
from tg_bot.adminka.callbacks.content import *
from tg_bot.adminka.callbacks.main import ContentCallback

from tg_bot.infra.database import async_session
from tg_bot.adminka.repositories.content import TextRepo, BannerRepo
from tg_bot.adminka.utils import parse_text

router = Router()


@router.callback_query(ContentCallback.filter(), StateFilter(default_state))
async def content_cmd(call: CallbackQuery):
    await call.message.edit_text(
        'Выберите группу которую хотите изменить',
        reply_markup=kb.select_content_type
    )


# ======================== TEXT HANDLERS ========================
@router.callback_query(TextEditCallback.filter(),
                       StateFilter(default_state, EditTextStates.text, EditTextStates.confirm))
async def text_edit_cmd(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        'Выберите поле для изменения',
        reply_markup=kb.select_text_field
    )


@router.callback_query(TextFieldCallback.filter(), StateFilter(default_state))
async def text_field_cmd(call: CallbackQuery, state: FSMContext, callback_data: TextFieldCallback):
    field = callback_data.field
    await state.set_state(EditTextStates.text)
    await state.update_data({'field': field})

    await call.message.edit_text(
        f'Пришлите новый текст для поля /{field}',
        reply_markup=kb.back_to_select_text_field
    )


@router.message(StateFilter(EditTextStates.text))
async def edit_text_text_cmd(message: Message, state: FSMContext):
    text = parse_text(message)
    await state.set_state(EditTextStates.confirm)
    await state.update_data({
        'text': text
    })
    await message.answer(text)
    await message.answer(
        'Вы уверены что хотите установить это сообщение?',
        reply_markup=kb.confirm_text_update
    )


@router.callback_query(TextFieldConfirmCallback.filter(), StateFilter(EditTextStates.confirm))
async def edit_text_text_confirm_cmd(call: CallbackQuery, callback_data: TextFieldCallback, state: FSMContext):
    data = await state.get_data()
    action = callback_data.action
    await state.clear()
    if not action:
        await call.message.edit_text(
            'Отменено', reply_markup=kb.back_to_select_text_field
        )
    else:
        async with async_session() as session:
            await TextRepo(session).update(key=data['field'], value=data['text'])
        await call.message.edit_text(
            'Новый тест установлен', reply_markup=kb.back_to_select_text_field
        )


# ======================== BANNER HANDLERS ========================
@router.callback_query(BannerEditCallback.filter(), StateFilter(default_state, EditBannerStates.banner))
async def text_edit_cmd(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        'Выберите поле для изменения',
        reply_markup=kb.select_banner_field
    )


@router.callback_query(BannerFieldCallback.filter(), StateFilter(default_state))
async def text_field_cmd(call: CallbackQuery, state: FSMContext, callback_data: TextFieldCallback):
    field = callback_data.field
    await state.set_state(EditBannerStates.banner)
    await state.update_data({'field': field})

    await call.message.edit_text(
        f'Пришлите новый текст для поля /{field}',
        reply_markup=kb.back_to_select_banner_field
    )


@router.message(StateFilter(EditBannerStates.banner))
async def edit_text_text_cmd(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer(
            'Пришлите фото, а не текст',
            reply_markup=kb.back_to_select_banner_field
        )
        return
    photo_id = message.photo[-1].file_id
    await state.set_state(EditBannerStates.confirm)
    await state.update_data({
        'banner': photo_id
    })
    await message.answer_photo(photo=photo_id)
    await message.answer(
        'Вы уверены что хотите установить это фото?',
        reply_markup=kb.confirm_banner_update
    )


@router.callback_query(BannerFieldConfirmCallback.filter(), StateFilter(EditBannerStates.confirm))
async def edit_text_text_confirm_cmd(call: CallbackQuery, callback_data: TextFieldCallback, state: FSMContext):
    data = await state.get_data()
    action = callback_data.action
    await state.clear()
    if not action:
        await call.message.edit_text(
            'Отменено', reply_markup=kb.back_to_select_banner_field
        )
    else:
        async with async_session() as session:
            await BannerRepo(session).update(key=data['field'], value=data['banner'])
        await call.message.edit_text(
            'Новое фото установлено', reply_markup=kb.back_to_select_banner_field
        )
