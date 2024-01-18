from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from api.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(128))
    email = Column(String(128))
    full_name = Column(String(128))
    password = Column(String(16))
    token = Column(String(32))
    created_at = Column(DateTime, default=datetime.utcnow)

    balance = Column(Float, default=100)

    chat = relationship("Chat", backref="user")