from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)

# Модель чеку продажу
class SalesCheck(Base):
    __tablename__ = "sales_checks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    products = relationship("SalesCheckProduct", back_populates="sales_check")
    payment_type = Column(String)
    payment_amount = Column(Float)

# Модель товару в чеку продажу
class SalesCheckProduct(Base):
    __tablename__ = "sales_check_products"

    id = Column(Integer, primary_key=True, index=True)
    sales_check_id = Column(Integer, ForeignKey('sales_checks.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Float)
    total = Column(Float)
    product = relationship("Product")
    sales_check = relationship("SalesCheck", back_populates="products")

# Клас для моделі вхідних даних для створення чеку продажу
class CreateSalesCheck(BaseModel):
    products: list[dict]
    payment_type: str
    payment_amount: float