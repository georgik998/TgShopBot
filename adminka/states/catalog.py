from aiogram.fsm.state import State, StatesGroup


class CategoryStates(StatesGroup):
    new_name = State()
    new_desc = State()
    edit_name = State()
    edit_desc = State()


class SubcategoryStates(StatesGroup):
    new_name = State()
    new_desc = State()
    edit_name = State()
    edit_desc = State()


class NewProductStates(StatesGroup):
    name = State()
    photo = State()
    description = State()
    price = State()
    file = State()


class EditProductStates(StatesGroup):
    name = State()
    photo = State()
    description = State()
    price = State()
    content = State()
