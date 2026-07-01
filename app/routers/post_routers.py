from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.jwt_handler import get_current_user
from app.schemas.post_schemas import PostsIn

post_router = APIRouter(tags=["posts"])



@post_router.post("/posts")
def create_post(post: PostsIn, user_id: Annotated[str, Depends(get_current_user)]):
    create_post_service(user_id, post)


@post_router.get("/posts")
def get_posts():
    pass

@post_router.get("/posts/")
def get_post(post: id):
    pass

@post_router.delete("/posts/")
def delete_post(post_id:str):
    pass

@post_router.patch("/posts/")
def update_post(post_id):
    pass

@post_router.patch("/posts/{post_id}")
def publish_post(post_id: str):
    pass


