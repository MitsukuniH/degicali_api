from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional

import api.models.goods_user as gu_model
import api.schemas.goods_user as gu_schema

async def get_goods_user(db:AsyncSession, goods_id: int) -> Optional[gu_model.GoodsUser]:
    result: Result = await db.execute(
        select(gu_model.GoodsUser).filter(gu_model.GoodsUser.goods_id == goods_id)
    )
    goods: Optional[Tuple[gu_model.GoodsUser]] = result.first()

    return goods[0] if goods is not None else None

async def get_goods_user_list(db:AsyncSession) -> List[Tuple[int, int, int]]:
    result: Result = await (
        db.execute(
            select(
                gu_model.GoodsUser.id,
                gu_model.GoodsUser.owner_id,
                gu_model.GoodsUser.goods_id
            )
        )
    )
    return result.all()

async def create_goods_user(
    db: AsyncSession, gu: gu_schema.GUBase
) -> gu_model.GoodsUser:
    gu = gu_model.GoodsUser(**gu.dict())
    db.add(gu)
    await db.commit()
    await db.refresh(gu)

    return gu

async def update_owner(
    db: AsyncSession, new_owner_id: int, original: gu_model.GoodsUser
) -> gu_schema.GUBase:
    original.owner_id = new_owner_id

    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original