from fastapi import Depends, HTTPException, status, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
import shutil
from api.db import get_db
import api.schemas.user as user_schema
import api.cruds.user as user_cruds
router = APIRouter()

@router.get("/user/{user_id}", response_model=user_schema.PublicUserInfo)
async def get_user(
    user_id:int, db: AsyncSession=Depends(get_db)
):
    user = await user_cruds.get_user_with_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="user not fount")
    
    return user

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

@router.get(
    "/users/{user_id}/image", 
    responses = {200: {"content": {"image/png": {}}}},
    response_class=Response
)
def get_uploadfile(
    user_id
):
    path = f'api/images/icon/{user_id}.png'
    file = open(path, "rb").read()
    if file is None:
        raise 
    return Response(content=file,media_type="image/png")

@router.post("/users/{user_id}/image")
def upload_image(
    user_id, image: UploadFile
):
    path = f'api/images/icon/{user_id}.png'
    with open(path, 'wb+') as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {
        'filename': path,
        'type': image.content_type
    }

@router.post("/user/me", response_model=user_schema.User)
async def read_users_me(
    auth_form:user_schema.AuthForm, db: AsyncSession=Depends(get_db)
):
    user = await user_cruds.get_user_with_token(db, auth_form)
    if user is None:
        raise HTTPException(status_code=404, detail="user not fount")
    
    return user