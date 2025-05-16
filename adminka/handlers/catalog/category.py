from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import StateFilter

from tg_bot.adminka.callbacks.catalog.category import *
from tg_bot.adminka.keyboards.catalog import category as kb
from tg_bot.adminka.states.catalog import CategoryStates

from tg_bot.infra.database import async_session
from tg_bot.adminka.repositories.catalog.category import CategoryRepo

from tg_bot.adminka.utils import parse_text

router = Router()


@router.callback_query(
    CategoryPanelCallback.filter(),
    StateFilter(
        default_state,
        CategoryStates.new_name, CategoryStates.new_desc,
    )
)
async def category_cmd(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        'Выберите действие',
        reply_markup=kb.category_panel
    )


# ======================== NEW: handlers for adding new category ========================
@router.callback_query(NewCategoryCallback.filter(), StateFilter(default_state))
async def new_category_cmd(call: CallbackQuery, state: FSMContext):
    await state.set_state(CategoryStates.new_name)
    await call.message.edit_text(
        'Пришлите название новой категории',
        reply_markup=kb.back_to_category_panel
    )


@router.message(StateFilter(CategoryStates.new_name))
async def new_category_name_cmd(message: Message, state: FSMContext):
    name = message.text
    async with async_session() as session:
        is_exists = await CategoryRepo(session).get_category_id_by_name(name)
    if is_exists:
        await message.answer(
            'Категория с таким именем уже существует, попробуйте снова',
            reply_markup=kb.back_to_category_panel
        )
        return
    else:
        await state.update_data({'name': name})
        await state.set_state(CategoryStates.new_desc)
        await message.answer(
            'Пришлите описание для категории',
            reply_markup=kb.back_to_category_panel
        )


@router.message(StateFilter(CategoryStates.new_desc))
async def new_category_desc_cmd(message: Message, state: FSMContext):
    description = message.text
    if len(description) >= 1024:
        await message.answer(
            'Максимальная длина описания 1024 символа, попробуйте снова',
            reply_markup=kb.back_to_category_panel
        )
        return
    name = await state.get_value('name')
    async with async_session() as session:
        await CategoryRepo(session).add_category(
            name=name,
            description=parse_text(message)
        )
    await state.clear()
    await message.answer(
        'Категория успешно добавлена!',
        reply_markup=kb.back_to_category_panel
    )


# ======================== EDIT: handlers for edit category ========================
@router.callback_query(
    EditCategoryCallback.filter(),
    StateFilter(
        default_state,
        CategoryStates.edit_name, CategoryStates.edit_desc
    )
)
async def edit_category_panel_cmd(call: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        categories = await CategoryRepo(session).get_categories()
    await state.clear()
    await call.message.edit_text(
        'Выберите действие для категории\n'
        '✏️ - изменить название\n'
        '📖 - изменить описание\n'
        '❌ - удалить',
        reply_markup=kb.build_category_manage_panel(data=categories)
    )


# ======== Delete ========
@router.callback_query(DeleteCategoryCallback.filter(), StateFilter(default_state))
async def edit_category_del_cmd(call: CallbackQuery, callback_data: DeleteCategoryCallback, state: FSMContext):
    category_id = callback_data.id
    await call.message.edit_text(
        'Вы уверены что хотите удалить категорию?\n'
        '❗️️<b><i>Это удалит все подкатегории и продукты привязанные к категории. Восстановить их не получится</i></b>',
        reply_markup=kb.confirm_delete_category(category_id)
    )


@router.callback_query(ConfirmDeleteCategoryCallback.filter(), StateFilter(default_state))
async def edit_category_del_confirm_cmd(call: CallbackQuery, callback_data: ConfirmDeleteCategoryCallback):
    category_id, action = callback_data.id, callback_data.action
    if not action:
        await call.message.edit_text(
            'Отменено',
            reply_markup=kb.back_to_category_edit_panel
        )
    else:
        async with async_session() as session:
            await CategoryRepo(session).delete_category(category_id)
        await call.message.edit_text(
            'Категория была удалена',
            reply_markup=kb.back_to_category_edit_panel
        )


# ======== Edit name ========
@router.callback_query(EditCategoryNameCallback.filter(), StateFilter(default_state))
async def edit_category_name_cmd(call: CallbackQuery, callback_data: EditCategoryNameCallback, state: FSMContext):
    await state.set_state(CategoryStates.edit_name)
    await state.update_data({'category_id': callback_data.id})
    await call.message.edit_text(
        'Пришлите новое название категории',
        reply_markup=kb.back_to_category_edit_panel
    )


@router.message(StateFilter(CategoryStates.edit_name))
async def edit_category_name_process_cmd(message: Message, state: FSMContext):
    name = message.text
    async with async_session() as session:
        await CategoryRepo(session).update_name(category_id=await state.get_value('category_id'), name=name)
    await state.clear()
    await message.answer(
        'Название было обновлено!',
        reply_markup=kb.back_to_category_edit_panel
    )


# ======== Edit description ========
@router.callback_query(
    EditCategoryDescriptionCallback.filter(),
    StateFilter(
        default_state
    )
)
async def edit_category_description_callback_cmd(
        call: CallbackQuery,
        callback_data: EditCategoryNameCallback,
        state: FSMContext
):
    await state.set_state(CategoryStates.edit_desc)
    await state.update_data({'category_id': callback_data.id})
    await call.message.edit_text(
        'Пришлите новое описание для категории',
        reply_markup=kb.back_to_category_edit_panel
    )


@router.message(
    StateFilter(
        CategoryStates.edit_desc
    )
)
async def edit_category_desc_process_cmd(
        message: Message,
        state: FSMContext
):
    description = message.text
    if len(description) >= 1024:
        await message.answer(
            'Максимальная длина описания 1024 символа',
            reply_markup=kb.back_to_category_edit_panel
        )
        return

    category_id = await state.get_value('category_id')
    async with async_session() as session:
        await CategoryRepo(session).patch_description(category_id, parse_text(message))

    await state.clear()
    await message.answer(
        'Описание успешно обновлено!',
        reply_markup=kb.back_to_category_edit_panel
    )
