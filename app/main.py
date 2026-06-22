from fastapi import FastAPI
from app.routers.auth_routers import auth_router
app = FastAPI()

app.include_router(auth_router)