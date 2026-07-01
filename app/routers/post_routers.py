from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from app.auth.jwt_handler import get_current_user
from app.schemas.post_schemas import PostsIn, CreatePostResponse, PostOut
from app.services.post_service import create_post_service, get_all_post_service, get_post_by_id_service

post_router = APIRouter(tags=["posts"])



@post_router.post("/posts", response_model=CreatePostResponse)
def create_post(post: PostsIn, user_id: Annotated[str, Depends(get_current_user)]):
    post_id = create_post_service(user_id, post)
    return {"post_id": post_id}


@post_router.get("/posts")
# access not restricted 
def get_posts():
    return get_all_post_service()
    
@post_router.get("/posts/{post_id}")
def get_post(post_id):
    try:
        post = get_post_by_id_service(post_id)
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UNEXPECTED ERROR OCCURED"
        )
    

@post_router.delete("/posts/")
def delete_post(post_id:str):
    pass

@post_router.patch("/posts/")
def update_post(post_id):
    pass

@post_router.patch("/posts/{post_id}")
def publish_post(post_id: str):
    pass


