from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Optional

import api.models.chat as chat_model
import api.schemas.chat as chat_schema

async def get_chat(db:AsyncSession, chat_id: int) -> Optional[chat_model.Chat]:
    result: Result = await db.execute(
        select(chat_model.Chat).filter(chat_model.Chat.id == chat_id)
    )
    chat: Optional[Tuple[chat_model.Chat]] = result.first()

    return chat[0] if chat is not None else None

async def get_chats(db:AsyncSession, user_id: int) -> List[Tuple[int, str, str, int]]:
    result: Result = await (
        db.execute(
            select(
                chat_model.Chat.id,
                chat_model.Chat.content,
                chat_model.Chat.community,
                chat_model.Chat.user_id,
                chat_model.Chat.posted_at
            ).filter(chat_model.Chat.user_id == user_id)
        )
    )
    return result.all()

async def get_chats_on_community(db:AsyncSession, community: str) -> List[Tuple[int, str, str, int]]:
    result: Result = await (
        db.execute(
            select(
                chat_model.Chat.id,
                chat_model.Chat.content,
                chat_model.Chat.community,
                chat_model.Chat.user_id,
                chat_model.Chat.posted_at
            ).filter(chat_model.Chat.community == community)
        )
    )
    return result.all()

async def create_chat(
    db: AsyncSession, chat_create: chat_schema.ChatCreate
) -> chat_model.Chat:
    chat = chat_model.Chat(**chat_create.dict())
    db.add(chat)
    await db.commit()
    await db.refresh(chat)

    return chat