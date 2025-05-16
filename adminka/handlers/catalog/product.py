from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import StateFilter
from typing import List

from io import BytesIO

from tg_bot.adminka.callbacks.catalog.product import *
from tg_bot.adminka.keyboards.catalog import product as kb
from tg_bot.adminka.states.catalog import NewProductStates, EditProductStates

from tg_bot.infra.database import async_session
from tg_bot.adminka.repositories.catalog.product import ProductRepo
from tg_bot.adminka.repositories.catalog.category import CategoryRepo
from tg_bot.adminka.repositories.catalog.subcategory import SubcategoryRepo

from tg_bot.adminka.utils import parse_text
from tg_bot.infra.database.models import product_name_max_length, product_description_max_length

router = Router()


@router.callback_query(ProductPanelCallback.filter(), StateFilter(default_state))
async def select_category_for_product_manage_cmd(call: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        categories = await CategoryRepo(session).get_categories()
    await call.message.edit_text(
        'Выберите категорию, для которой хотите управлять товарами',
        reply_markup=kb.select_category_for_product_manage(categories)
    )


@router.callback_query(SelectCategoryForProductCallback.filter(), StateFilter(default_state))
async def select_subcategory_for_product_manage_cmd(call: CallbackQuery,
                                                    callback_data: SelectCategoryForProductCallback, state: FSMContext):
    category_id, subcategory_id = callback_data.category_id, callback_data.subcategory_id
    async with async_session() as session:
        if subcategory_id:
            category_id = await SubcategoryRepo(session).get_category_id_by_subcategory_id(subcategory_id)
        subcategories = await SubcategoryRepo(session).get_subcategories_by_category_id(category_id)
    await call.message.edit_text(
        'Выберите подкатегорию, для которой хотите управлять товарами',
        reply_markup=kb.select_subcategory_for_product_manage(subcategories)
    )


# ======================== PRODUCT MANAGE PANEL ========================
@router.callback_query(SelectSubcategoryForProductCallback.filter(), StateFilter(default_state, NewProductStates.name))
async def product_panel_cmd(call: CallbackQuery, callback_data: SelectSubcategoryForProductCallback, state: FSMContext):
    subcategory_id = callback_data.subcategory_id
    async with async_session() as session:
        product = await ProductRepo(session).get_all_by_subcategory_id(subcategory_id)
    await state.clear()
    if call.message.photo:  # если вернулись из управлением продуктом
        await call.message.delete()
        await call.message.answer(
            'Выберите действие для товара\n'
            '✏️ - редактирование\n'
            '❌ - удалить',
            reply_markup=kb.products_manage(product, subcategory_id)
        )
    else:
        await call.message.edit_text(
            'Выберите действие для товара\n'
            '✏️ - редактирование\n'
            '❌ - удалить',
            reply_markup=kb.products_manage(product, subcategory_id)
        )


# ======================== NEW PRODUCT ========================
@router.callback_query(NewProductCallback.filter(), StateFilter(default_state))
async def new_product_name_request_cmd(call: CallbackQuery, callback_data: NewProductCallback, state: FSMContext):
    subcategory_id = callback_data.subcategory_id
    await state.update_data({'subcategory_id': subcategory_id})
    await state.set_state(NewProductStates.name)
    await call.message.edit_text(
        'Введи название для нового продукта',
        reply_markup=kb.back_to_product_manage(subcategory_id)
    )


@router.message(StateFilter(NewProductStates.name))
async def new_product_photo_request_cmd(message: Message, state: FSMContext):
    if len(message.text) > product_name_max_length:
        await message.answer(
            f'Длина описания не может превышать {product_name_max_length} символа, попробуйте снова'
        )
        return
    await state.update_data({
        'name': message.text
    })
    await state.set_state(NewProductStates.photo)
    await message.answer(
        'Отлично! Теперь пришлите фото товара'
    )


@router.message(StateFilter(NewProductStates.photo))
async def new_product_description_request_cmd(message: Message, state: FSMContext):
    await state.update_data({
        'photo': message.photo[-1].file_id
    })
    await state.set_state(NewProductStates.description)
    await message.answer(
        'Отлично! Теперь пришлите описание товара'
    )


@router.message(StateFilter(NewProductStates.description))
async def new_product_price_request_cmd(message: Message, state: FSMContext):
    if len(message.text) > product_description_max_length:
        await message.answer(
            f'Длина описания не может превышать {product_description_max_length} символа, попробуйте снова'
        )
        return
    await state.update_data({
        'description': parse_text(message)
    })
    await state.set_state(NewProductStates.file)
    await message.answer(
        'Отлично! Теперь пришлите файл с контентом для товара'
    )


@router.message(StateFilter(NewProductStates.file))
async def new_product_file_cmd(message: Message, state: FSMContext, bot: Bot):
    if not message.document:
        await message.answer('А где файл? Попробуйте снова')
        return

    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    file_content = BytesIO(downloaded_file.getvalue()).read().decode('utf-8')
    content: List[str] = file_content.splitlines()

    await state.update_data({'content': content})
    await state.set_state(NewProductStates.price)
    await message.answer(
        'Отлично! Теперь пришлите цену товара'
    )


@router.message(StateFilter(NewProductStates.price))
async def new_product_post_cmd(message: Message, state: FSMContext):
    try:
        price = float(message.text.replace(',', '.'))
    except ValueError:
        await message.answer('Цена должна быть числом, попробуйте снова')
        return
    data = await state.get_data()
    async with async_session() as session:
        await ProductRepo(session).post(
            subcategory_id=data['subcategory_id'],
            name=data['name'],
            description=data['description'],
            photo=data['photo'],
            price=price,
            content=data['content']
        )
    await state.clear()
    await message.answer(
        'Отлично! Товар добавлен!',
        reply_markup=kb.back_to_product_manage(data['subcategory_id'])
    )


# ======================== DELETE PRODUCT ========================
@router.callback_query(DeleteProductCallback.filter(), StateFilter(default_state))
async def delete_product_cmd(call: CallbackQuery, callback_data: DeleteProductCallback, state: FSMContext):
    product_id, subcategory_id = callback_data.product_id, callback_data.subcategory_id
    await call.message.edit_text(
        'Вы уверены что хотите удалить продукт?\n'
        '❗️<b><i>Восстановить его не получится</i></b>',
        reply_markup=kb.confirm_delete_product(product_id, subcategory_id)
    )


@router.callback_query(ConfirmDeleteProductCallback.filter(), StateFilter(default_state))
async def confirm_delete_product_cmd(call: CallbackQuery, callback_data: ConfirmDeleteProductCallback):
    action, product_id, subcategory_id = callback_data.action, callback_data.product_id, callback_data.subcategory_id
    if not action:
        await call.message.edit_text(
            'Отменено',
            reply_markup=kb.back_to_product_manage(subcategory_id)
        )
    else:
        async with async_session() as session:
            await ProductRepo(session).delete(product_id)
        await call.message.edit_text(
            'Продукт удален',
            reply_markup=kb.back_to_product_manage(subcategory_id)
        )


# ======================== EDIT PRODUCT ========================
@router.callback_query(
    EditProductCallback.filter(),
    StateFilter(
        default_state,
        EditProductStates.content,
        EditProductStates.photo,
        EditProductStates.price,
        EditProductStates.name,
        EditProductStates.description
    )
)
async def edit_product_panel_cmd(call: CallbackQuery, callback_data: EditProductCallback, state: FSMContext):
    product_id, subcategory_id = callback_data.product_id, callback_data.subcategory_id
    async with async_session() as session:
        product = await ProductRepo(session).get(product_id)
    await state.clear()
    await call.message.edit_media(
        media=InputMediaPhoto(
            media=product.photo,
            caption=product.description
        ),
        reply_markup=kb.product_edit(product, subcategory_id)
    )


@router.callback_query(EditProductItem.filter(), StateFilter(default_state))
async def edit_product_item_cmd(call: CallbackQuery, callback_data: EditProductItem, state: FSMContext, ):
    product_id, subcategory_id, action = callback_data.product_id, callback_data.subcategory_id, callback_data.action
    text = 'error404'
    match action:
        case 'content':
            text = ('Пришлите .txt файл с новым наполнением для продукт\n'
                    'Каждая строчка - 1 наполнение')
            await state.set_state(EditProductStates.content)
        case 'photo':
            text = 'Новое фото для продукта'
            await state.set_state(EditProductStates.photo)
        case 'price':
            text = 'Пришлите новую цену для продукта'
            await state.set_state(EditProductStates.price)
        case 'name':
            text = 'Пришлите новое название для продукта'
            await state.set_state(EditProductStates.name)
        case 'description':
            text = 'Пришлите новое описание для продукта'
            await state.set_state(EditProductStates.description)
    await state.update_data({
        'product_id': product_id,
        'subcategory_id': subcategory_id,
        'action': action
    })
    await call.message.delete()
    await call.message.answer(
        text=text,
        reply_markup=kb.back_to_product_edit(product_id, subcategory_id)
    )


@router.message(EditProductStates.content)
async def edit_product_item_content_cmd(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    product_id, subcategory_id, action = data['product_id'], data['subcategory_id'], data['action']

    if not message.document:
        await message.answer('А где файл? Попробуйте снова',
                             reply_markup=kb.back_to_product_edit(product_id, subcategory_id))
        return

    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    file_content = BytesIO(downloaded_file.getvalue()).read().decode('utf-8')
    content = file_content.splitlines()

    async with async_session() as session:
        await ProductRepo(session).post_content(product_id, content[::-1])

    await state.clear()
    await message.answer(
        text='Данные о продукте обновлены!',
        reply_markup=kb.back_to_product_edit(product_id, subcategory_id)
    )


@router.message(EditProductStates.photo)
async def edit_product_item_photo_cmd(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id, subcategory_id, action = data['product_id'], data['subcategory_id'], data['action']

    if not message.photo:
        await message.answer('А где фото? Попробуйте снова',
                             reply_markup=kb.back_to_product_edit(product_id, subcategory_id))
        return

    async with async_session() as session:
        await ProductRepo(session).patch(col=action, value=message.photo[-1].file_id, product_id=product_id)

    await state.clear()
    await message.answer(
        text='Данные о продукте обновлены!',
        reply_markup=kb.back_to_product_edit(product_id, subcategory_id)
    )


@router.message(EditProductStates.price)
async def edit_product_item_price_cmd(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id, subcategory_id, action = data['product_id'], data['subcategory_id'], data['action']

    try:
        price = float(message.text.replace(',', '.'))
    except ValueError:
        await message.answer('Цена должна быть числом. Попробуйте снова',
                             reply_markup=kb.back_to_product_edit(product_id, subcategory_id))
        return

    async with async_session() as session:
        await ProductRepo(session).patch(col=action, value=price, product_id=product_id)

    await state.clear()
    await message.answer(
        text='Данные о продукте обновлены!',
        reply_markup=kb.back_to_product_edit(product_id, subcategory_id)
    )


@router.message(EditProductStates.name)
async def edit_product_item_name_cmd(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id, subcategory_id, action = data['product_id'], data['subcategory_id'], data['action']

    if len(message.text) > product_name_max_length:
        await message.answer(
            f'Слишком длинное название, сделайте его короче или не больше {product_name_max_length} символов',
            reply_markup=kb.back_to_product_edit(product_id, subcategory_id))
        return

    async with async_session() as session:
        await ProductRepo(session).patch(col=action, value=message.text, product_id=product_id)

    await state.clear()
    await message.answer(
        text='Данные о продукте обновлены!',
        reply_markup=kb.back_to_product_edit(product_id, subcategory_id)
    )


@router.message(EditProductStates.description)
async def edit_product_item_description_cmd(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id, subcategory_id, action = data['product_id'], data['subcategory_id'], data['action']

    if len(message.text) > product_description_max_length:
        await message.answer(
            f'Слишком длинное описание, сделайте его короче или не больше {product_description_max_length} символов',
            reply_markup=kb.back_to_product_edit(product_id, subcategory_id))
        return

    async with async_session() as session:
        await ProductRepo(session).patch(col=action, value=parse_text(message), product_id=product_id)

    await state.clear()
    await message.answer(
        text='Данные о продукте обновлены!',
        reply_markup=kb.back_to_product_edit(product_id, subcategory_id)
    )
