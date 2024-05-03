from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.user_models import User, Token, CreateUser
from models.sales_models import Product, SalesCheck, SalesCheckProduct, CreateSalesCheck
from services.user_services import authenticate_user, create_access_token, pwd_context
from services.conect_db_services import get_db
from fastapi import Depends, HTTPException, status
from services.user_services import get_current_user

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


@app.post("/sales-check", response_model=dict)
async def create_sales_check(sales_check_data: CreateSalesCheck, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Получение ID текущего пользователя
    user_id = current_user.id

    # Создание объекта чека продажи с указанием user_id
    sales_check = SalesCheck(payment_type=sales_check_data.payment_type, payment_amount=sales_check_data.payment_amount, user_id=user_id)

    # Добавление товаров в чек из входных данных
    for product_info in sales_check_data.products:
        product_name = product_info.get("name")
        product_price = product_info.get("price")
        product_quantity = product_info.get("quantity")

        # Добавить товар в чек
        sales_check_product = SalesCheckProduct(product=Product(name=product_name, price=product_price), quantity=product_quantity, total=product_price * product_quantity)
        sales_check.products.append(sales_check_product)

    # Расчет общей суммы чека
    total = sum(product_info.get("price", 0) * product_info.get("quantity", 0) for product_info in sales_check_data.products)

    # Проверка наличия достаточной суммы для оплаты
    if total > sales_check.payment_amount:
        raise HTTPException(status_code=400, detail=f"Insufficient funds. Total amount: {total}, Payment amount: {sales_check.payment_amount}")

    # Сохранение чека продажи в базе данных
    db.add(sales_check)
    db.commit()
    db.refresh(sales_check)

    # Подготовка ответа
    response_data = {
        "id": sales_check.id,
        "user_id": sales_check.user_id,  # Добавлено поле user_id в ответ
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