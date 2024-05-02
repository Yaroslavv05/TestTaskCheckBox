# Функція для розрахунку вартості позицій в чеку та загальної суми
def calculate_sales_check(products):
    total = 0
    for item in products:
        item['total'] = item['price'] * item['quantity']
        total += item['total']
    return total