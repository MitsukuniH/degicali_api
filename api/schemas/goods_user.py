from pydantic import BaseModel, Field

class GUBase(BaseModel):
    owner_id: int = Field(None, example=1)
    goods_id: int = Field(None, example=1)

class GU(GUBase):
    id: int

    class Config:
        orm_mode = True