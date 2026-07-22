from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse
from typing import Annotated, List
from uuid import UUID

from app.auth.jwt_handler import get_current_user
from app.services.post_service import create_post_service
from app.exceptions.post_exception import BlogException
from app.schemas.post_schemas import *


post_router = APIRouter(tags=["posts"])
from app.schemas.post_schemas import *


@post_router.post("/posts", response_model=PostOut)
def create_post(post_in: PostIn, user_id: Annotated[UUID, Depends(get_current_user)]):
    try:
        return create_post_service(user_id, post_in)
    except BlogException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@post_router.delete("/posts", response_model=FeedbackOut)
def delete_post(content_id:UUID, user_id: Annotated[UUID, Depends(get_current_user)]):
    try:
        return delete_post_service(user_id, content_id)
    except BlogException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        


@post_router.patch("/posts")
def update_post():
    pass

@post_router.get("/posts/")
def get_all_posts():
    pass

@post_router.get("/posts")
def get_post():
    pass