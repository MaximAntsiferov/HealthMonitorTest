from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    id: Optional[int] = None
    email: str
    created_at: date
    updated_at: date
    hashed_password: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: EmailStr
