from app.schemas.post_schemas import PostIn, PostOut
from app.exceptions.post_exception import *
from app.repositories.post_repos import (
    create_post_repo,
    )

def create_post_service(user_id, post_in: PostIn):
    post = create_post_repo(user_id,post_in.title, post_in.content)
    if post is None:
        raise PostOperationError("Faild to create post, please try again")
    else:
        return PostOut(**post)

    
        