from datetime import datetime
from typing import List
from fastapi import status, APIRouter, Depends, Response
from sqlalchemy import and_

from source.db import tests, database
from source.models.tests import Test, TestCreate, TestUpdate
from source.models.user import BaseUser
from source.services.auth import get_current_user

router = APIRouter(prefix="/tests", tags=["Tests"])


@router.post("/create", response_model=Test, status_code=status.HTTP_201_CREATED, )
async def create_test(test_data: TestCreate, user: BaseUser = Depends(get_current_user)):
    """
    Добавление нового теста
    """
    now = datetime.utcnow()
    test = Test(
        created_at=now,
        updated_at=now,
        user=user.id,
        **test_data.dict(),
    )
    values = {**test.dict()}
    values.pop("id", None)
    query = tests.insert().values(**values)
    test_id = await database.execute(query)
    get_created_test = tests.select().where(tests.c.id == test_id)
    created_test = await database.fetch_one(get_created_test)
    return created_test


@router.get("/", response_model=List[Test])
async def get_tests():
    """
    Получение списка выполненных тестов

    """
    query = tests.select()
    tests_list = await database.fetch_all(query)
    return tests_list


@router.get("/{test_id}", response_model=Test)
async def get_test(test_id: int):
    """
    Получение теста по ID
    - **test_id** - ID рецепта
    """
    query = tests.select().where(tests.c.id == test_id)
    return await database.fetch_one(query)


@router.put('/{recipe_id}', response_model=Test)
async def update_test(test_id: int, test_data: TestUpdate, user: BaseUser = Depends(get_current_user)):
    """
    Изменение характеристик теста
    - **test_id** - ID изменяемого теста
    """
    now = datetime.utcnow()
    test_data.dict()['update_at'] = now
    query = tests.update().where(and_(tests.c.id == test_id, tests.c.user == user.id)).values(**test_data.dict())
    await database.execute(query)
    get_updated_test = tests.select().where(tests.c.id == test_id)
    updated_test = await database.fetch_one(get_updated_test)
    return updated_test


@router.delete('/{test_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_test(test_id: int, user: BaseUser = Depends(get_current_user)):
    """
    Удаление рецепта
    - **recipe_id** - ID удаляемого рецепта
    """
    query = tests.delete().where(and_(tests.c.id == test_id, tests.c.user == user.id))
    await database.execute(query)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


