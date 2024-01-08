from fastapi import APIRouter

router = APIRouter()

@router.get("/user/{user_id}")
async def list_user():
    pass

@router.post("/user")
async def create_user():
    pass

@router.put("/user/{user_id}")
async def update_user():
    pass

@router.delete("/user/{user_id}")
async def delete_task():
    pass