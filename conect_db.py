from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

 
# Підключення до бази даних з використанням SQLAlchemy
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:55dnBZ72x@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# З'єднання з базою даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()