from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from api.db import Base

class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    describe = Column(String(524))
    category = Column(Integer)
    price = Column(Float)
    posted_at = Column(DateTime, default=datetime.utcnow)

