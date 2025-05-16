from aiogram import Router

from tg_bot.adminka.handlers.main import router as main_router
from tg_bot.adminka.handlers.subscribe_channels import router as subscribe_channels_router
from tg_bot.adminka.handlers.notify_channels import router as notify_channels_router
from tg_bot.adminka.handlers.user import router as user_router
from tg_bot.adminka.handlers.admin import router as admin_router
from tg_bot.adminka.handlers.spam import router as spam_router
from tg_bot.adminka.handlers.content import router as content_router
from tg_bot.adminka.handlers.faq import router as faq_router
from tg_bot.adminka.handlers.promocodes import router as promocodes_router
from tg_bot.adminka.handlers.catalog import router as catalog_router
from tg_bot.adminka.handlers.contact import router as contact_router
from tg_bot.adminka.handlers.statistic import router as statistic_router
from tg_bot.adminka.handlers.ref_links import router as ref_links_router

from tg_bot.adminka.filter.is_admin import IsAdminFilter

router = Router()
router.include_routers(
    subscribe_channels_router,
    notify_channels_router,
    user_router,
    admin_router,
    spam_router,
    content_router,
    faq_router,
    promocodes_router,
    catalog_router,
    contact_router,
    statistic_router,
    ref_links_router,
    main_router
)

router.message.filter(IsAdminFilter())
router.callback_query.filter(IsAdminFilter())
