from fastapi import FastAPI
from app.routers.auth_routers import auth_router
from app.routers.user_routers import user_router
from app.routers.tags_routers import tag_router
from app.routers.post_routers import post_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(tag_router)
app.include_router(post_router)