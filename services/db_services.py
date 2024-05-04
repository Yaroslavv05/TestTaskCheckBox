from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


"""
This code snippet defines a function called `get_db` that is used to create a database session. 

The function creates a SQLAlchemy engine using the provided `SQLALCHEMY_DATABASE_URL` and then creates a sessionmaker object called `SessionLocal` with the engine. 

When the `get_db` function is called, it creates a new session using `SessionLocal` and yields it. The session is closed using the `finally` block to ensure that it is always closed, even if an exception occurs.

This code snippet is useful for managing database sessions in a SQLAlchemy application.
"""

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:55dnBZ72x@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()