from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.user_models import User, Token, CreateUser
from models.sales_models import Product, SalesCheck, SalesCheckProduct, CreateSalesCheck
from services.user_services import authenticate_user, create_access_token, pwd_context
from services.sales_services import calculate_sales_check
from conect_db import get_db

# Ініціалізація FastAPI
app = FastAPI()


# Реєстрація користувача
@app.post("/register")
async def register_user(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(name=user.name, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return {"message": "User successfully registered"}


# Авторизація користувача та отримання JWT токена
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Оновлений ендпоінт для створення чеку продажу
@app.post("/sales-check", response_model=dict)
async def create_sales_check(sales_check_data: CreateSalesCheck, db: Session = Depends(get_db)):
    # Отримання ідентифікатора користувача з токена аутентифікації
    # Це приклад. Потрібно додати логіку для отримання user_id з токена
    user_id = 1  # Приклад: тимчасове значення для user_id

    # Створення об'єкта чеку продажу
    sales_check = SalesCheck(user_id=user_id, payment_type=sales_check_data.payment.type, payment_amount=sales_check_data.payment.amount)

    # Додавання товарів до чеку
    for product_info in sales_check_data.products:
        product = db.query(Product).filter(Product.name == product_info.name).first()
        if product:
            sales_check_product = SalesCheckProduct(product_id=product.id, quantity=product_info.quantity, total=product_info.price * product_info.quantity)
            sales_check.products.append(sales_check_product)
        else:
            raise HTTPException(status_code=404, detail=f"Product '{product_info.name}' not found")

    # Розрахунок загальної суми чеку
    total = sum(product_info.price * product_info.quantity for product_info in sales_check_data.products)

    # Збереження чеку продажу в базу даних
    db.add(sales_check)
    db.commit()
    db.refresh(sales_check)

    # Підготовка відповіді
    response_data = {
        "id": sales_check.id,
        "products": [
            {
                "name": product.product.name,
                "price": product.product.price,
                "quantity": product.quantity,
                "total": product.total,
                "additional_info": product_info.additional_info
            }
            for product, product_info in zip(sales_check.products, sales_check_data.products)
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