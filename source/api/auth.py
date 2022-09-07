from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from source.db import users, database
from source.models.token import Token
from source.models.user import UserCreate, BaseUser
from source.services.auth import get_password_hash, create_access_token, authenticate_user, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/sign-up", response_model=Token, status_code=status.HTTP_201_CREATED)
async def sign_up(user_data: UserCreate):
    """
    Регистрация нового пользователя
    """
    now = datetime.utcnow()
    user = BaseUser(
        created_at=now,
        updated_at=now,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
    )
    values = {**user.dict()}
    values.pop("id", None)
    query = users.insert().values(**values)
    await database.execute(query)
    access_token = create_access_token(data={'sub': user.email})
    token = {"access_token": access_token, "token_type": "bearer"}
    return token


@router.post("/sign-in", response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Авторизация
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    token = {"access_token": access_token, "token_type": "bearer"}
    return token


@router.get("/profile", response_model=BaseUser)
async def profile(current_user: BaseUser = Depends(get_current_user)):
    """
    Вход в профиль пользователя
    """
    return current_user
