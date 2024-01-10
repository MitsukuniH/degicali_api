from sqlalchemy import Column, Integer
from api.db import Base

class GoodsUser(Base):
    __tablename__ = "goods_user"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    goods_id = Column(Integer)