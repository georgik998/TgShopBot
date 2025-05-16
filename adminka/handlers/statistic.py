from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.filters.state import StateFilter

from tg_bot.adminka.callbacks.main import StatisticCallback
from tg_bot.adminka.keyboards.main import back_to_admin_kb

from tg_bot.infra.database import async_session
from tg_bot.adminka.repositories.user import UserRepo, UserPurchasesRepo
from tg_bot.adminka.repositories.payment import PaymentRepo
from tg_bot.adminka.repositories.catalog.product import ProductRepo

from datetime import timedelta

router = Router()


@router.callback_query(StatisticCallback.filter(), StateFilter(default_state))
async def statistic_cmd(call: CallbackQuery):
    async with async_session() as session:
        user_statistic = await UserRepo(session).get_statistic()
        products_statistic = await ProductRepo(session).get_statistic()
        payments_statistic = await PaymentRepo(session).get_statistic()
    text = f"""📊Статистика
    
🦣 <b><i>ЮЗЕРЫ</i></b>
<blockquote>👥 Всего юзеров:
 <b>{user_statistic["total_users"]}</b>
 
⏳ Дата регистрации последнего юзера: 
<i>{(user_statistic["last_registration"] + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M:%S")}</i>

⛔️ Заблокированных юзеров:
{user_statistic["blocked_users"]} ~ {user_statistic["blocked_users_percent"]}%

💸 Общий баланс всех юзеров:
 <code>{user_statistic["total_balance"]}₽</code>
 
📅 Новых юзеров за
    -сегодня: <b>{user_statistic["today_users"]}</b>
    -неделю: <b>{user_statistic["week_users"]}</b>
    -месяц: <b>{user_statistic["month_users"]}</b></blockquote>

🛍 <b><i>ТОВАРЫ</i></b>
<blockquote>🛒 Всего товаров:
<b>{products_statistic["total_products"]}</b>

📈 Средняя стоимость:
<code>{products_statistic["average_price"]}₽</code>

💸 Потенциальная прибыль
(если продадим все товары по текущей цене) 
<code>{products_statistic["potential_revenue"]}₽</code></blockquote>

💎<b><i>ПОПОЛНЕНИЯ</i></b>
<blockquote>📈Всего транзакций:
<b>{payments_statistic["total_transactions"]}</b>

🪪Процент успешных пополнений: 
<b>{payments_statistic["success_transactions_percent"]}%</b>
    
🌍Самый популярный платежный метод:
<i>{payments_statistic["popular_system"]}</i>

🧾 Средняя сумма пополнения:
<code>{payments_statistic["average_amount"]}₽</code>

👑 Самое большое пополнения:
    - Cумма: <code>{payments_statistic["max_transaction"]["amount"]}₽</code>
    - tg_id: <code>{payments_statistic["max_transaction"]["tg_id"]}</code></blockquote>
"""
    await call.message.edit_text(
        text=text,
        reply_markup=back_to_admin_kb
    )

# 💸 <b><i>Пополнения</i></b>
# <blockquote>
#
# </blockquote>
#
# 🛍 <b><i>ТОВАРЫ</i></b>
# <blockquote>
#
# </blockquote>
