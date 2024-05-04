from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from .user_models import User

Base = declarative_base()

'''
Base: SQLAlchemy declarative base for defining database models.

Product: SQLAlchemy model for representing products in the database, including ID, name, and price.

SalesCheck: SQLAlchemy model for representing sales checks in the database, including ID, user ID, creation timestamp, 
payment type, payment amount, and relationship with SalesCheckProduct.

SalesCheckProduct: SQLAlchemy model for representing products within a sales check, including ID, sales check ID, product ID,
quantity, total amount, and relationships with Product and SalesCheck.
'''

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)

class SalesCheck(Base):
    __tablename__ = "sales_checks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id))
    created_at = Column(DateTime, default=datetime.utcnow)
    products = relationship("SalesCheckProduct", back_populates="sales_check")
    payment_type = Column(String)
    payment_amount = Column(Float)

class SalesCheckProduct(Base):
    __tablename__ = "sales_check_products"

    id = Column(Integer, primary_key=True, index=True)
    sales_check_id = Column(Integer, ForeignKey('sales_checks.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Float)
    total = Column(Float)
    product = relationship("Product")
    sales_check = relationship("SalesCheck", back_populates="products")
