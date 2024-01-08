from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from api.db import Base

class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    describe = Column(String(524))
    type = Column(Integer)
    price = Column(Float)
    posted_at = Column(DateTime, default=datetime.utcnow)

