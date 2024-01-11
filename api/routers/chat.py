from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.schemas.chat as chat_schema
import api.cruds.chat as chat_crud

from api.db import get_db

router = APIRouter()

@router.get("/chats/community/{community_id}", response_model=List[chat_schema.Chat])
async def chats_on_community(
    community: str, db:AsyncSession=Depends(get_db)
):
    return await chat_crud.get_chats_on_community(db, community=community)

@router.get("/chats/user/{user_id}", response_model=List[chat_schema.Chat])
async def chats_on_user(
    user_id: int, db:AsyncSession=Depends(get_db)
):
    return await chat_crud.get_chats(db, user_id=user_id)

@router.get("/chat/{chat_id}", response_model=chat_schema.Chat)
async def chat(
    chat_id: int, db:AsyncSession=Depends(get_db)
):
    chat = await chat_crud.get_chat(db, chat_id=chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    
    return chat

@router.post("/chat", response_model=chat_schema.Chat)
async def create_chat(
    chat_body: chat_schema.ChatBase, db: AsyncSession = Depends(get_db)
):
    chat = await chat_crud.create_chat(db, chat_body)
    
    return chat