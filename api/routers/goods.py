from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.schemas.goods as goods_schema
import api.schemas.goods_user as gu_schema
import api.cruds.goods as goods_crud
import api.cruds.goods_user as gu_crud

from api.db import get_db

router = APIRouter()

@router.get("/goods", response_model=List[goods_schema.Goods])
async def list_goods(
    db:AsyncSession=Depends(get_db)
):
    
    return await goods_crud.get_goods_list(db)

@router.get("/goods/{goods_id}", response_model=goods_schema.GoodsOwner)
async def goods(
    goods_id: int, db:AsyncSession=Depends(get_db)
):
    goods = await goods_crud.get_goods(db, goods_id=goods_id)
    if goods is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    
    res = goods.__dict__
    res["owner_id"] = (await gu_crud.get_goods_user(db, goods_id)).owner_id
    return res

@router.post("/goods", response_model=goods_schema.GoodsCreateResponse)
async def create_goods(
    goods_body: goods_schema.GoodsCreate, db: AsyncSession = Depends(get_db)
):
    goods = await goods_crud.create_goods(db, goods_body)
    
    return goods

@router.put("/goods/{goods_id}", response_model=goods_schema.GoodsCreateResponse)
async def update_goods(
    goods_id: int, goods_name: goods_schema.GoodsUpdate, db: AsyncSession = Depends(get_db)
):
    goods = await goods_crud.get_goods(db, goods_id=goods_id)
    if goods is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    
    return await goods_crud.update_goods(db, goods_name, original=goods)

@router.delete("/goods/{goods_id}", response_model=None)
async def delete_task(
    goods_id: int, db:AsyncSession=Depends(get_db)
):
    goods = await goods_crud.get_goods(db, goods_id=goods_id)
    if goods is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    
    return await goods_crud.delete_goods(db, original=goods)