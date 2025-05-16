from aiogram import Router

from tg_bot.handlers.user.main import router as main_router
from tg_bot.handlers.user.profile import router as profile_router
from tg_bot.handlers.user.catalog import router as catalog_router
from tg_bot.handlers.user.payment import router as payment_router

router = Router()

router.include_routers(

    main_router,
    payment_router,
    profile_router,
    catalog_router,

)
