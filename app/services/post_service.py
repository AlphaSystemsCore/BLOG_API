from app.schemas.post_schemas import PostIn
from app.repositories.post_repos import (
    create_post_repo,
    )

def create_post_service(user_id, post_in: PostIn):
    feedback = create_post_repo(user_id,post_in.title, post_in.content)
    if feedback == "content_failed":
        