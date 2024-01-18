from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
import random, string

import api.schemas.user as user_schema
import api.models.user as user_model


async def get_user_with_name(db:AsyncSession, username: str):
    result: Result = await db.execute(
        select(user_model.User).filter(user_model.User.username == username)
    )
    user_dict = result.first()
    if user_dict is None:
        return None
    return user_dict[0]

async def get_user_with_id(db: AsyncSession, id:int):
    result: Result = await db.execute(
        select(user_model.User).filter(user_model.User.id == id)
    )
    user_dict = result.first()
    if user_dict is None:
        return None
    return user_dict[0]

async def get_user_with_token(db: AsyncSession, form_data:user_schema.AuthForm):
    result: Result = await db.execute(
        select(user_model.User).filter(user_model.User.id == form_data.id)
    )
    user_dict = result.first()
    if user_dict is None:
        return None
    
    if user_dict[0].token != form_data.token:
        return None
    return user_dict[0]

async def user_auth(db: AsyncSession, form_data:user_schema.SignInForm):
    result: Result = await db.execute(
        select(user_model.User).filter(user_model.User.username == form_data.username)
    )
    user_dict = result.first()
    if user_dict is None:
        return None
    if user_dict[0].password != form_data.password:
        return None
    
    return user_dict[0]

async def create_user(
    db: AsyncSession, user_create: user_schema.SignUpForm
) -> user_model.User:
    raw_user = user_create.dict()
    raw_user["token"] = create_token(32)
    user = user_model.User(**raw_user)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

def create_token(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

async def update_user(
    db: AsyncSession, update: user_schema.UserUpdate, original: user_model.User
) -> user_model.User:
    original.username = update.username
    original.email = update.email
    original.balance = update.balance

    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original