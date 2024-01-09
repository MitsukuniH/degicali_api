from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter

from api.db import get_db
import api.schemas.user as user_schema
import api.cruds.user as user_cruds
router = APIRouter()

@router.get("/user/{user_id}", response_model=user_schema.PublicUserInfo)
async def get_user(
    user_id:int, db: AsyncSession=Depends(get_db)
):
    return await user_cruds.get_user_with_id(db, user_id)

@router.put("/user/me")
async def update_user():
    pass

@router.delete("/user/{user_id}")
async def delete_task():
    pass

@router.post("/sign_up", response_model=user_schema.Token)
async def login_for_access_token(
    form_data: user_schema.SignUpForm,
    db: AsyncSession=Depends(get_db)
):
    user = await user_cruds.get_user_with_name(db, form_data.username)
    if user is not None:
        raise HTTPException(status_code=500, detail="This username already exist.")
    
    return await user_cruds.create_user(db, form_data)

@router.post("/sign_in", response_model=user_schema.Token)
async def login_for_access_token(
    form_data: user_schema.SignInForm,
    db: AsyncSession=Depends(get_db)
):
    user = await user_cruds.user_auth(db, form_data)
    if user is None:
        raise HTTPException(status_code=404, detail="user not fount")
    
    return user

@router.post("/users/me/", response_model=user_schema.User)
async def read_users_me(
    auth_form:user_schema.AuthForm, db: AsyncSession=Depends(get_db)
):
    return await user_cruds.get_user_with_token(db, auth_form)