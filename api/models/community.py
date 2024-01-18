from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
from api.db import Base

class Community(Base):
    __tablename__ = "communities"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    describe = Column(String(524))

    goods = relationship("Goods", backref="communities")
    chat = relationship("Chat", backref="communities")