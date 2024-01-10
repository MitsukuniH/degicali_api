from pydantic import BaseModel, Field
from datetime import datetime

class GoodsBase(BaseModel):
    name: str = Field(None, example="photo_1")
    describe: str = Field("", example="cute cat photo!")
    category: int = Field(None, ge=0, le=3, example=0)
    price: float = Field(None, ge=0, example=0.1)

class GoodsUpdate(BaseModel):
    name: str = Field(None, example="photo_1")
    describe: str = Field("", example="cute cat photo!")
    price: float = Field(None, ge=0, example=0.1)

class GoodsCreate(GoodsBase):
    owner_id: int

class GoodsCreateResponse(GoodsBase):
    id: int
    posted_at: datetime

    class Config:
        orm_mode = True
    
class Goods(GoodsBase):
    id: int
    posted_at: datetime

    class Config:
        orm_mode = True

class GoodsOwner(Goods):
    owner_id: int