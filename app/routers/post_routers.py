from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse
from typing import Annotated, List


post_router = APIRouter(tags=["posts"])
from app.schemas.post_schemas import *
from app.auth.jwt_handler import get_current_user

@post_router.post("/posts")
def create_post(post_in: PostIn, user_id: Annotated[str, Depends(get_current_user)]):
    pass

@post_router.delete("/posts")
def delete_post(content_id:str, user_id: Annotated[str, Depends(get_current_user)]):
    pass

@post_router.patch("/posts")
def update_post():
    pass

@post_router.get("/posts/")
def get_all_posts():
    pass

@post_router.get("/posts")
def get_post()