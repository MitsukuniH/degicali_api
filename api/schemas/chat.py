from pydantic import BaseModel, Field
from datetime import datetime

class ChatBase(BaseModel):
    user_id: int = Field(None, example=1)
    content: str = Field(None, example="cute cat")
    community_id: int = Field(None, example=0)

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int
    posted_at: datetime

    class Config:
        orm_mode = True