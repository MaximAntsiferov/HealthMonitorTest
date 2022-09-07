from datetime import date
from typing import Optional

from pydantic import BaseModel, PositiveInt


class Test(BaseModel):
    id: Optional[int] = None
    user: int
    created_at: date
    updated_at: date
    acet: PositiveInt
    keto: int
    rpm: int

    class Config:
        orm_mode = True


class TestCreate(BaseModel):
    acet: PositiveInt
    keto: int
    rpm: int

    class Config:
        orm_mode = True


class TestUpdate(TestCreate):
    pass