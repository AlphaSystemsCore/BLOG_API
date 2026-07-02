from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.jwt_handler import get_current_user

like_router = APIRouter()
# to continue from here.
@like_router.post("/likes")
def like_post(post):
    return "to be implemented"