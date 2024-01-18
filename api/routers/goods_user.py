from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.schemas.goods_user as gu_schema
import api.cruds.goods_user as gu_crud
import api.schemas.user as user_schema
import api.cruds.user as user_crud
import api.schemas.goods as goods_schema
import api.cruds.goods as goods_crud

from api.db import get_db

router = APIRouter()

@router.get("/goods_users", response_model=List[gu_schema.GU])
async def list_goods_users(
    db:AsyncSession=Depends(get_db)
):
    
    return await gu_crud.get_goods_user_list(db)

@router.post("/goods_user", response_model=gu_schema.GU)
async def create_goods(
    gu_body: gu_schema.GUBase, db: AsyncSession = Depends(get_db)
):
    return await gu_crud.create_goods_user(db=db, gu=gu_schema.GUBase(owner_id=gu_body.owner_id, goods_id=gu_body.goods_id))

@router.put("/goods_user/{goods_id}", response_model=gu_schema.GU)
async def update_goods(
    goods_id: int, new_owner_id: int, user_token: user_schema.Token, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user_with_token(db, user_token)
    if user is None:
        raise HTTPException(status_code=500, detail="User could not be authenticated")
    
    new_owner = await user_crud.get_user_with_id(db, new_owner_id)
    if new_owner is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    gu = await gu_crud.get_goods_user(db, goods_id=goods_id)
    if gu is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    
    return await gu_crud.update_owner(db, new_owner_id=new_owner_id, original=gu)

@router.put("/buy/{goods_id}", response_model=gu_schema.GU)
async def update_goods(
    goods_id: int, user_token: user_schema.Token, db: AsyncSession = Depends(get_db)
):
    
    user = await user_crud.get_user_with_token(db, user_token)
    if user is None:
        raise HTTPException(status_code=500, detail="User could not be authenticated")
    
    goods = await goods_crud.get_goods(db, goods_id=goods_id)
    if goods is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    
    if user.balance < goods.price:
        raise HTTPException(status_code=501, detail="Not enough balance")
    
    user = await user_crud.update_user(
        db, user_schema.UserUpdate(**{"username":user.username, "email":user.email, "balance":user.balance-goods.price}), user
    )
    gu = await gu_crud.get_goods_user(db, goods_id=goods_id)
    if gu is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    
    return await gu_crud.update_owner(db, new_owner_id=user.id, original=gu)

@router.put("/toggle_sale/{goods_id}", response_model=goods_schema.GoodsSale)
async def toggle_sale(
    goods_id: int, user_token: user_schema.Token, db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_user_with_token(db, user_token)
    if user is None:
        raise HTTPException(status_code=500, detail="User could not be authenticated")
    
    goods = await goods_crud.get_goods(db, goods_id=goods_id)
    if goods is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    
    return await goods_crud.toggle_sale(db, goods)