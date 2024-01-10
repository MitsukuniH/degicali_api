from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional

import api.models.goods as goods_model
import api.models.goods_user as gu_model
import api.schemas.goods as goods_schema

async def get_goods(db:AsyncSession, goods_id: int) -> Optional[goods_model.Goods]:
    result: Result = await db.execute(
        select(goods_model.Goods).filter(goods_model.Goods.id == goods_id)
    )
    goods: Optional[Tuple[goods_model.Goods]] = result.first()

    return goods[0] if goods is not None else None

async def get_goods_list(db:AsyncSession) -> List[Tuple[int, str, int]]:
    result: Result = await (
        db.execute(
            select(
                goods_model.Goods.id,
                goods_model.Goods.name,
                goods_model.Goods.category,
                goods_model.Goods.price,
                goods_model.Goods.posted_at
            )
        )
    )
    return result.all()

async def create_goods(
    db: AsyncSession, goods_create: goods_schema.GoodsCreate
) -> goods_model.Goods:
    dict_goods = goods_create.dict()
    dict_goods.pop("owner_id")
    goods = goods_model.Goods(**dict_goods)
    db.add(goods)
    await db.commit()
    await db.refresh(goods)

    return goods

async def update_goods(
    db: AsyncSession, update: goods_schema.GoodsUpdate, original: goods_model.Goods
) -> goods_model.Goods:
    original.name = update.name
    original.describe = update.describe
    original.price = update.price

    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_goods(
    db: AsyncSession, original: goods_model.Goods
) -> None:
    await db.delete(original)
    await db.commit()