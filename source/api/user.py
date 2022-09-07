from datetime import datetime
from typing import List
from fastapi import status, APIRouter, Depends, Response
from sqlalchemy import and_


from source.db import database, users
from source.models.user import User, BaseUser, UserUpdate
from source.services.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
async def get_users():
    """
    Получение списка пользователей

    """
    users_query = users.select()
    user_list = await database.fetch_all(users_query)
    return user_list


@router.put('/{user_id}', response_model=User)
async def update_user(user_id: int, user_data: UserUpdate, user: BaseUser = Depends(get_current_user)):
    """
    Изменение характеристик пользователя
    - **user_id** - ID пользователя
    """
    now = datetime.utcnow()
    user_data.dict()['update_at'] = now
    query = users.update().where(and_(users.c.id == user.id, users.c.id == user_id)).values(**user_data.dict())
    await database.execute(query)
    get_updated_user = users.select().where(and_(users.c.id == user.id, users.c.id == user_id))
    updated_user = await database.fetch_one(get_updated_user)
    return updated_user


@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: int):
    """
    Получение пользователя по ID
    - **user_id** - ID пользователя
    """
    user_query = users.select().where(and_(users.c.id == user_id, users.c.id == user_id))
    user = await database.fetch_one(user_query)
    return user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user: BaseUser = Depends(get_current_user)):
    """
    Удаление пользователя
    """
    query = users.delete().where(and_(users.c.id == user_id, users.c.id == user.id))
    await database.execute(query)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



