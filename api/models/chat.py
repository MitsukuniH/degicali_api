from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from api.db import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    content = Column(String(1024))
    posted_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.id'))
    community_id = Column(Integer, ForeignKey('communities.id'), nullable=True)