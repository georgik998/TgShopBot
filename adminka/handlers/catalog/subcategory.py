from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import StateFilter

from tg_bot.adminka.callbacks.catalog.subcategory import *
from tg_bot.adminka.keyboards.catalog import subcategory as kb
from tg_bot.adminka.states.catalog import SubcategoryStates

from tg_bot.infra.database import async_session
from tg_bot.adminka.repositories.catalog.subcategory import SubcategoryRepo
from tg_bot.adminka.repositories.catalog.category import CategoryRepo

from tg_bot.adminka.utils import parse_text

router = Router()


@router.callback_query(SubcategoryPanelCallback.filter(), )
async def edit_subcategory_panel_cmd(call: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        categories = await CategoryRepo(session).get_categories()
    await state.clear()
    await call.message.edit_text(
        'Выберите категорию для которой хотите редактировать подкатегорию',
        reply_markup=kb.build_category_select_panel(categories=categories)
    )


# ======================== EDIT: handlers for edit subcategory ========================
@router.callback_query(
    SelectCategoryForSubcategoryEditPanelCallback.filter(),
    StateFilter(
        default_state,
        SubcategoryStates.edit_name, SubcategoryStates.edit_desc,
        SubcategoryStates.new_name, SubcategoryStates.new_desc
    )
)
async def edit_subcategory_panel_select_category_cmd(call: CallbackQuery,
                                                     callback_data: SelectCategoryForSubcategoryEditPanelCallback,
                                                     state: FSMContext):
    category_id = callback_data.id
    async with async_session() as session:
        subcategories = await SubcategoryRepo(session).get_subcategories_by_category_id(category_id)
    await state.clear()
    await call.message.edit_text(
        'Выберите действие для подкатегории\n'
        '✏️ - изменить название\n'
        '📖 - изменить описание\n'
        '❌ - удалить',
        reply_markup=kb.build_subcategory_manage_panel(subcategories, category_id)
    )


# ======== Delete ========
@router.callback_query(DeleteSubcategoryCallback.filter(), StateFilter(default_state))
async def edit_subcategory_del_cmd(call: CallbackQuery, callback_data: DeleteSubcategoryCallback, state: FSMContext):
    subcategory_id, category_id = callback_data.id, callback_data.category_id
    await call.message.edit_text(
        'Вы уверены что хотите удалить категорию?\n'
        '❗️️<b><i>Это удалит подкатегорию и продукты привязанные к подкатегории. Восстановить их не получится</i></b>',
        reply_markup=kb.confirm_delete_subcategory(subcategory_id, category_id)
    )


@router.callback_query(ConfirmDeleteSubcategoryCallback.filter(), StateFilter(default_state))
async def edit_subcategory_del_confirm_cmd(call: CallbackQuery, callback_data: ConfirmDeleteSubcategoryCallback):
    subcategory_id, action, category_id = callback_data.id, callback_data.action, callback_data.category_id
    if not action:
        await call.message.edit_text(
            'Отменено',
            reply_markup=kb.back_to_subcategory_edit_panel(category_id)
        )
    else:
        async with async_session() as session:
            await SubcategoryRepo(session).delete_subcategory(subcategory_id)
        await call.message.edit_text(
            'Подкатегория была удалена',
            reply_markup=kb.back_to_subcategory_edit_panel(category_id)
        )


# ======== Edit name ========
@router.callback_query(EditSubcategoryNameCallback.filter(), StateFilter(default_state))
async def edit_subcategory_name_cmd(call: CallbackQuery, callback_data: EditSubcategoryNameCallback, state: FSMContext):
    subcategory_id, category_id = callback_data.id, callback_data.category_id
    await state.set_state(SubcategoryStates.edit_name)
    await state.update_data({
        'subcategory_id': subcategory_id,
        'category_id': category_id
    })
    await call.message.edit_text(
        'Пришлите новое имя для подкатегории',
        reply_markup=kb.back_to_subcategory_edit_panel(category_id=category_id)
    )


@router.message(SubcategoryStates.edit_name)
async def edit_subcategory_name_process_cmd(message: Message, state: FSMContext):
    async with async_session() as session:
        await SubcategoryRepo(session).update_name(
            subcategory_id=await state.get_value('subcategory_id'),
            name=message.text
        )
    category_id = await state.get_value('category_id')
    await state.clear()
    await message.answer(
        'Название было обновлено!',
        reply_markup=kb.back_to_subcategory_edit_panel(category_id=category_id)
    )


# ======== Edit description ========
@router.callback_query(EditSubcategoryDescriptionCallback.filter(), StateFilter(default_state))
async def edit_subcategory_description_cmd(
        call: CallbackQuery,
        callback_data: EditSubcategoryDescriptionCallback,
        state: FSMContext
):
    subcategory_id, category_id = callback_data.id, callback_data.category_id
    await state.set_state(SubcategoryStates.edit_desc)
    await state.update_data({
        'subcategory_id': subcategory_id,
        'category_id': category_id
    })
    await call.message.edit_text(
        'Пришлите новое описание для подкатегории',
        reply_markup=kb.back_to_subcategory_edit_panel(category_id=category_id)
    )


@router.message(StateFilter(SubcategoryStates.edit_desc))
async def edit_subcategory_description_process_cmd(
        message: Message,
        state: FSMContext
):
    data = await state.get_data()
    description = message.text
    if len(description) >= 1024:
        await message.answer(
            'Описание не может быть длиннее 1024 символов, попробуйте снова',
            reply_markup=kb.back_to_subcategory_edit_panel(category_id=data['category_id'])
        )
        return
    async with async_session() as session:
        await SubcategoryRepo(session).update_description(
            subcategory_id=data['subcategory_id'],
            description=parse_text(message)
        )
    await message.answer(
        'Описание было обновлено!',
        reply_markup=kb.back_to_subcategory_edit_panel(category_id=data['category_id'])
    )


# ======================== NEW: handlers for adding new category ========================
@router.callback_query(NewSubcategoryCallback.filter(), StateFilter(default_state))
async def edit_subcategory_new_cmd(call: CallbackQuery, callback_data: NewSubcategoryCallback, state: FSMContext):
    category_id = callback_data.category_id
    await state.set_state(SubcategoryStates.new_name)
    await state.update_data({
        'category_id': category_id
    })
    await call.message.edit_text(
        'Пришлите название новой подкатегории',
        reply_markup=kb.back_to_subcategory_edit_panel(category_id)
    )


@router.message(StateFilter(SubcategoryStates.new_name))
async def edit_subcategory_new_process_cmd(message: Message, state: FSMContext):
    category_id = await state.get_value('category_id')
    name = message.text
    async  with async_session() as session:
        is_exists = await SubcategoryRepo(session).get_subcategory_id_by_name(name)
    if is_exists:
        await message.answer(
            'Подкатегория с таким именем уже существует, попробуйте другое название',
            reply_markup=kb.back_to_subcategory_edit_panel(category_id)
        )
        return
    await state.update_data({'name': name})
    await state.set_state(SubcategoryStates.new_desc)
    await message.answer(
        'Пришлите описание для новой подкатегории',
        reply_markup=kb.back_to_subcategory_edit_panel(category_id)
    )


@router.message(StateFilter(SubcategoryStates.new_desc))
async def edit_subcategory_new_process_cmd(message: Message, state: FSMContext):
    data = await state.get_data()
    description = message.text
    if len(description) >= 1024:
        await message.answer(
            'Описание не может быть длиннее 1024 символов, попробуйте снова',
            reply_markup=kb.back_to_subcategory_edit_panel(data['category_id'])
        )
        return
    async with async_session() as session:
        await SubcategoryRepo(session).add_subcategory(
            name=message.text, category_id=data['category_id'],description=parse_text(message)
        )
    await state.clear()
    await message.answer(
        'Подкатегория успешно добавлена!',
        reply_markup=kb.back_to_subcategory_edit_panel(data['category_id'])
    )
