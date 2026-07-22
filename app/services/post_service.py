from uuid import UUID

from app.schemas.post_schemas import PostIn, PostOut, FeedbackOut
from app.exceptions.post_exception import *
from app.repositories.post_repos import (
    create_post_repo,
    delete_post_repo,
    )

def create_post_service(user_id, post_in: PostIn):
    """create a fresh post and return the created post"""
    post = create_post_repo(user_id,post_in.title, post_in.content)
    if post is None:
        raise PostOperationError("Faild to create post, please try again")
    else:
        return PostOut(**post)

def delete_post_service(user_id: UUID, content_id: UUID):
    """deletes post that satisfys the user_id and content_id"""
    row_count = delete_post_repo(user_id, content_id)
    if row_count == 0:
        raise PostOperationError("Failed to delete post, please try again")
    return FeedbackOut(content_id = content_id, message = "deleted")

    
        