from tg_bot.utils import round_number

texts = {
    'not_found_product': 'Ой-ой! Пока товара нет в наличии, попробуйте позже',
    'select_category': '▼ Для продолжения нажмите на нужную вам категорию:',
    'select_subcategory': 'Выберите подкатегорию',
    'low_balance': lambda price_delta: f'Для оплаты заказа на вашем балансе не хватает - {price_delta}₽',
    'content_not_available': 'Произошла ошибка, попробуйте снова',
    'success_purchase': lambda purchase_id: f"Ваш заказ №<code>{purchase_id}</code> успешно собран! Поздравляем!",
    'activate_promo': '🎁 <b>Активация промокода</b>\n\n▼ Пришлите в ответ промокод:',
    'not_found_promo': '💢 <b>Введённый промокод не найден</b>\n\n▼ Отмените ввод / Попробуйте ввести промокод повторно:',
    'success_promo': lambda old_price, new_price, name: f"""<b>🎁 Промокод успешно активирован для товара: {name}</b>

💥 <b>Новая цена: {new_price}</b>
Старая цена: <del>{old_price}</del>""",
    'product': lambda name, price, description: f"""<b>Товар:</b> {name}
    
{description}

<b>💰 Цена:</b> <code>{round_number(price)} RUB</code>"""
}
