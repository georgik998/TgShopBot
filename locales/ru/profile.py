texts = {
    "main": lambda tg_id, reg_date, balance, referral_balance, purchases, purchases_amount: f"""👤 <b>Профиль</b>
<blockquote>├• ID: <code>{tg_id}</code>
╰• Регистрация: <code>{reg_date.strftime("%d-%m-%Y")}</code></blockquote>

💰 <b>Баланс</b>
<blockquote>├• Основной: <code>{balance} RUB</code>
╰• Реферальный:  <code>{referral_balance} RUB</code></blockquote>

📊 <b>Статистика</b>
<blockquote>├• Сумма покупок: <code>{purchases_amount} RUB</code>
╰• Кол-во покупок: <code>{purchases}</code></blockquote>""",
    "ref_system_description": lambda ref_balance, total_ref, ref_link: f"""👥 <b>Реферальная программа</b>
Возможность получать на баланс 5% от пополнений ваших рефералов.

<blockquote>ℹ️ <b>Информация</b></blockquote>
 ├• Количество рефералов: <b>{total_ref}</b>
 ╰• Реферальный баланс: <b>{ref_balance} ₽</b>

<b>Ссылка:</b> <code>{ref_link}</code>
""",
    'activate_promo': '🎁 <b>Активация промокода</b>\n\n▼ Пришлите в ответ промокод:',
    'not_found_promo': '💢 <b>Введённый промокод не найден</b>\n\n▼ Отмените ввод / Попробуйте ввести промокод повторно:',
    'success_promo': lambda amount: f"""🎁 <b>Промокод успешно активирован!</b>

На ваш баланс зачислено: <code>{amount} RUB</code>""",
    'promo_error_type': """⚠️ <b>Введённый промокод не подходит для пополнения баланса!</b>

▼ Для активации промокода выберите интересующий вас товар""",
    "my_purchase": lambda order_id, product_name, product_price: f"""🔖 <b>Заказ</b> №<code>{order_id}</code>

Товар: <b>{product_name}</b>

Кол-во: <b>1 шт</b>
Сумма: <b>{product_price}₽</b>"""
}
