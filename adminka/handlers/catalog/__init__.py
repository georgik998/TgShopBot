from aiogram import Router

from tg_bot.adminka.handlers.catalog.main import router as main_router
from tg_bot.adminka.handlers.catalog.category import router as category_router
from tg_bot.adminka.handlers.catalog.subcategory import router as subcategory_router
from tg_bot.adminka.handlers.catalog.product import router as product_router

router = Router()

router.include_routers(
    category_router,
    subcategory_router,
    product_router,
    main_router
)
