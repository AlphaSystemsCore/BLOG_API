from app.schemas.post_schemas import PostsIn
from app.repositories.post_repos import create_post_repo

def create_post_service(user_id, post: PostsIn):
        post_id = create_post_repo(user_id, post.title, post.content)
        return post_id
    

    

