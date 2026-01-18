import datetime as dt
from decimal import Decimal
from datetime import timedelta, date


def add(items, title, amount, expiration_date=None):
    if expiration_date:
        expiration_date = dt.datetime.strptime(expiration_date, '%Y-%m-%d').date()
    items.setdefault(title, []).append({
        'amount': amount,
        'expiration_date': expiration_date
    })


def add_by_note(items, note):
    parts = note.split()
    
    if len(parts) < 2:
        raise ValueError(f"Некорректный формат записи. Ожидается: 'Название количество дата'. Получено: '{note}'")
    
    last_part = parts[-1]
    is_date = False
    try:
        dt.datetime.strptime(last_part, '%Y-%m-%d')
        is_date = True
    except ValueError:
        if last_part.lower() == 'none':
            is_date = True
    
    if is_date:
        exp_date = parts[-1]
        amount_str = parts[-2]
        title = ' '.join(parts[:-2])
    else:
        exp_date = None
        amount_str = parts[-1]
        title = ' '.join(parts[:-1])
    
    amount = Decimal(amount_str)
    
    expiration_date = None if exp_date and exp_date.lower() == 'none' else exp_date
    
    add(items, title, amount, expiration_date)


def find(items, needle):
    needle_lower = needle.lower()
    return [product for product in items if needle_lower in product.lower()]


def amount(items, needle):
    found_products = find(items, needle)
    total_amount = Decimal(0)
    for product in found_products:
        for batch in items.get(product, []):
            total_amount += batch['amount']
    return total_amount


def expire(items, in_advance_days=0):
    today = date.today() + timedelta(days=in_advance_days)
    expired_products = []
    for title, batches in items.items():
        for batch in batches:
            if batch['expiration_date'] and batch['expiration_date'] < today:
                expired_products.append(title)
                break
    return expired_products


storage = {}
add(storage, 'Яйца Фабрики №1', Decimal('4'), '2023-07-15')
print(storage)


goods = {}


add_by_note(goods, 'Сыр 0.3 2023-07-25')
add_by_note(goods, 'Сок 1 None')


add_by_note(goods, 'Яйца Фабрики №1 4 2023-07-15')


print(goods)


print(find(goods, 'Сыр'))
print(find(goods, 'Яйца'))


print(amount(goods, 'Сок'))
print(amount(goods, 'Яйца'))


print(expire(goods, 10))  # проверка просрочки на 10 дней вперед
