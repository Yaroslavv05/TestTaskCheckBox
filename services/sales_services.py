from fastapi import HTTPException, Depends, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from models.user_models import User
from models.sales_models import Product, SalesCheck, SalesCheckProduct
from schemas.sales_schemas import CreateSalesCheck
from services.user_services import get_current_user
from services.db_services import get_db
from fastapi import Depends, HTTPException

'''
create_sales_check: Creates a new sales check in the database, validates payment, and returns details of the created check.

get_sales_checks: Retrieves sales checks based on various criteria and returns details including total count.

get_sales_check_by_id: Retrieves a specific sales check by ID and validates ownership, returning its details.

view_sales_check: Retrieves a sales check by ID and generates a text receipt, calculating total and due amounts.
'''

async def create_sales_check(sales_check_data: CreateSalesCheck, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.id

    sales_check = SalesCheck(payment_type=sales_check_data.payment_type, payment_amount=sales_check_data.payment_amount, user_id=user_id)

    for product_info in sales_check_data.products:
        product_name = product_info.get("name")
        product_price = product_info.get("price")
        product_quantity = product_info.get("quantity")

        sales_check_product = SalesCheckProduct(product=Product(name=product_name, price=product_price), quantity=product_quantity, total=product_price * product_quantity)
        sales_check.products.append(sales_check_product)

    total = sum(product_info.get("price", 0) * product_info.get("quantity", 0) for product_info in sales_check_data.products)

    if total > sales_check.payment_amount:
        raise HTTPException(status_code=400, detail=f"Insufficient funds. Total amount: {total}, Payment amount: {sales_check.payment_amount}")
    
    db.add(sales_check)
    db.commit()
    db.refresh(sales_check)

    response_data = {
        "id": sales_check.id,
        "products": [
            {
                "name": product.product.name,
                "price": product.product.price,
                "quantity": product.quantity,
                "total": product.total,
            }
            for product in sales_check.products
        ],
        "payment": {
            "type": sales_check.payment_type,
            "amount": sales_check.payment_amount
        },
        "total": total,
        "rest": sales_check.payment_amount - total,
        "created_at": sales_check.created_at
    }

    return response_data


async def get_sales_checks(start_date: str = Query(None), end_date: str = Query(None), min_total: int = Query(None), payment_type: str = Query(None), limit: int = Query(10), offset: int = Query(0), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(SalesCheck).filter(SalesCheck.user_id == current_user.id)

    if start_date:
        query = query.filter(SalesCheck.created_at >= start_date)
    if end_date:
        query = query.filter(SalesCheck.created_at <= end_date)
    if min_total:
        query = query.filter(SalesCheck.payment_amount >= min_total)
    if payment_type:
        query = query.filter(SalesCheck.payment_type == payment_type)

    total = query.count()

    query = query.limit(limit).offset(offset)

    sales_checks = query.all()

    response_data = {
        "total": total,
        "sales_checks": [
            {
                "id": sales_check.id,
                "user_id": sales_check.user_id,
                "created_at": sales_check.created_at,
                "products": [
                    {
                        "name": sales_check_product.product.name,
                        "price": sales_check_product.product.price,
                        "quantity": sales_check_product.quantity,
                        "total": sales_check_product.total,
                    }
                    for sales_check_product in sales_check.products
                ],
                "payment": {
                    "type": sales_check.payment_type,
                    "amount": sales_check.payment_amount
                },
                "total": sum(sales_check_product.total for sales_check_product in sales_check.products),
                "rest": sales_check.payment_amount - sum(sales_check_product.total for sales_check_product in sales_check.products),
            }
            for sales_check in sales_checks
        ]
    }
    
    return response_data


async def get_sales_check_by_id(sales_check_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    found_sales_check = None
    all_sales_checks = db.query(SalesCheck).all()
    for check in all_sales_checks:
        if check.id == sales_check_id and check.user_id == current_user.id:
            found_sales_check = check
            break

    if not found_sales_check:
        raise HTTPException(status_code=404, detail="Sales check not found")

    response_data = {
        "id": found_sales_check.id,
        "user_id": found_sales_check.user_id,
        "created_at": found_sales_check.created_at,
        "products": [
            {
                "name": sales_check_product.product.name,
                "price": sales_check_product.product.price,
                "quantity": sales_check_product.quantity,
                "total": sales_check_product.total,
            }
            for sales_check_product in found_sales_check.products
        ],
        "payment": {
            "type": found_sales_check.payment_type,
            "amount": found_sales_check.payment_amount
        },
        "total": sum(sales_check_product.total for sales_check_product in found_sales_check.products),
        "rest": found_sales_check.payment_amount - sum(sales_check_product.total for sales_check_product in found_sales_check.products),
    }

    return response_data


async def view_sales_check(sales_check_id: int, db: Session = Depends(get_db)):
    sales_check = db.query(SalesCheck).filter(SalesCheck.id == sales_check_id).first()
    if not sales_check:
        raise HTTPException(status_code=404, detail="Sales check not found")
    
    total_amount = sum(item.total for item in sales_check.products)

    due_amount = total_amount - sales_check.payment_amount

    check_text = f"""
      ФОП Джонсонюк Борис       
================================
"""

    for item in sales_check.products:
        check_text += f"{item.quantity:.2f} x {item.product.price:.2f}\n"
        check_text += f"{item.product.name:<20} {item.total:>12,.2f}\n"
        check_text += f"{'-' * 32}\n"

    check_text += f"""
================================
{"СУМА":<20} {total_amount:>12,.2f}
{f"{'Готівка' if sales_check.payment_type=='cash' else 'Картка'}":<20} {sales_check.payment_amount:>12,.2f}
{"Решта":<20} {due_amount:>12,.2f}
================================
        {sales_check.created_at.strftime('%d.%m.%Y %H:%M')}
      Дякуємо за покупку!       

    """

    return PlainTextResponse(check_text)