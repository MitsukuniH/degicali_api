from fastapi import FastAPI
from api.routers import user
from api.routers import goods
from api.routers import goods_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user.router)
app.include_router(goods.router)
app.include_router(goods_user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 許可するオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)