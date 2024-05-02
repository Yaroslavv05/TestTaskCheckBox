from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.sales_models import Product

# Підключення до бази даних
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:55dnBZ72x@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Створення сесії
db = SessionLocal()

# Створення тестових товарів
products_data = [
    {"name": "Яблуко", "price": 50.0},
    {"name": "Апельсин", "price": 30.0},
    {"name": "Банан", "price": 40.0},
]

try:
    # Додавання товарів до бази даних
    for product_info in products_data:
        product = Product(name=product_info["name"], price=product_info["price"])
        db.add(product)
    
    # Збереження змін у базі даних
    db.commit()
    print("Товари успішно додані до бази даних.")
except Exception as e:
    print(f"Сталася помилка: {e}")
finally:
    db.close()
    