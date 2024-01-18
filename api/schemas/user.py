from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class Token(BaseModel):
    id: int
    token: str

    class Config:
        orm_mode = True

class AuthForm(BaseModel):
    id: int
    token: str

class UserUpdate(BaseModel):
    username: str
    email:str
    balance: float

class SignInForm(BaseModel):
    username: str
    password: str

class SignUpForm(SignInForm):
    email: str
    full_name: str

class PublicUserInfo(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True

class User(PublicUserInfo):
    email: str
    full_name: str
    balance: float


class UserInDB(User):
    password: str