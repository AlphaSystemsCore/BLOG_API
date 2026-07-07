from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List

from app.auth.jwt_handler import get_current_user
from app.schemas.post_schemas import PostsIn, SuccessAction, PostOut
from app.services.post_service import create_post_service, get_all_post_service, get_post_by_id_service, get_post_by_title_service, delete_post_service
from app.exceptions.post_exception import *

post_router = APIRouter(tags=["posts"])



@post_router.post("/posts", response_model=SuccessAction)
def create_post(post: PostsIn, user_id: Annotated[str, Depends(get_current_user)]):
    try:
        feedback = create_post_service(user_id, post)
    except FailedToCreatePostError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED_ERROR_OCCURED"

        )
    return feedback


@post_router.get("/posts",response_model=List[PostOut])
# access not restricted 
def get_posts():

    return get_all_post_service()
    
@post_router.get("/posts/{post_id}")
def get_post(post_id):
    post = get_post_by_id_service(post_id)
    return post

@post_router.get("/posts/")
def get_post_by_title(title:str):
    post = get_post_by_title_service(title)
    return post

    
@post_router.delete("/posts/", response_model=SuccessAction)
def delete_post(post_id:str, user_id: Annotated[str, Depends(get_current_user)]):
    feedback = delete_post_service(user_i, post_id)
    return feedback


@post_router.patch("/posts/{post_id}")
def publish_post(post_id: str, user_id: Annotated[str, Depends(get_current_user)]):
    # to be implemented
    pass

