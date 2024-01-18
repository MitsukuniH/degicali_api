from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.schemas.community as community_schema
import api.cruds.community as community_crud

from api.db import get_db

router = APIRouter()

@router.get("/community", response_model=List[community_schema.Community])
async def list_community(
    db:AsyncSession=Depends(get_db)
):
    
    return await community_crud.get_community_list(db)

@router.get("/community/{community_id}", response_model=community_schema.Community)
async def community(
    community_id: int, db:AsyncSession=Depends(get_db)
):
    community = await community_crud.get_community(db, community_id=community_id)
    if community is None:
        raise HTTPException(status_code=404, detail="community not found")

    return community

@router.post("/community", response_model=community_schema.Community)
async def create_community(
    community_body: community_schema.CommunityCreate, db: AsyncSession = Depends(get_db)
):
    community = await community_crud.create_community(db, community_body)
    
    return community


@router.get(
    "/community/{community_id}/image", 
    responses = {200: {"content": {"image/png": {}}}},
    response_class=Response
)
def get_uploadfile(
    community_id
):
    path = f'api/images/community/{community_id}.png'
    file = open(path, "rb").read()
    if file is None:
        raise 
    return Response(content=file,media_type="image/png")