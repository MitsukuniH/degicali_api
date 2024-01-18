from pydantic import BaseModel, Field

class CommunityBase(BaseModel):
    name: str = Field(None, example="cat")
    describe: str = Field(None, example="discribe")

class CommunityCreate(CommunityBase):
    pass

class Community(CommunityBase):
    id: int = Field(None, example=0)

    class Config:
        orm_mode = True