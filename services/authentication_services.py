from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.user_models import User
from schemas.user_shemas import CreateUser
from .user_services import authenticate_user, create_access_token, pwd_context
from .db_services import get_db
from fastapi import Depends, HTTPException, status

'''
These asynchronous functions handle user registration and login processes.

The register_user function hashes the user's password, creates a new user instance with the hashed password, 

adds it to the database session, and commits the transaction.

The login_for_access_token function checks the user's credentials, generates an access token 

if the user is authenticated, and returns it along with the token type.
'''

async def register_user(user: CreateUser, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким же username
    existing_user = get_user_by_username(user.username, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already exists. Please choose another one.",
        )    
    # Если пользователя с таким username не существует, продолжаем регистрацию
    hashed_password = pwd_context.hash(user.password)
    db_user = User(name=user.name, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return {"message": "User successfully registered"}

def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()


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

