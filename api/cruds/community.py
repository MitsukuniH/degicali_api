from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional

import api.models.community as community_model
import api.schemas.community as community_schema

async def get_community(db:AsyncSession, community_id: int) -> Optional[community_model.Community]:
    result: Result = await db.execute(
        select(community_model.Community).filter(community_model.Community.id == community_id)
    )
    community: Optional[Tuple[community_model.Community]] = result.first()

    return community[0] if community is not None else None

async def get_community_list(db:AsyncSession) -> List[Tuple[int, str, int]]:
    result: Result = await (
        db.execute(
            select(
                community_model.Community.id,
                community_model.Community.name,
                community_model.Community.describe
            )
        )
    )
    return result.all()

async def create_community(
    db: AsyncSession, community_create: community_schema.CommunityCreate
) -> community_model.Community:
    community = community_model.Community(**community_create.dict())
    db.add(community)
    await db.commit()
    await db.refresh(community)

    return community