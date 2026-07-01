from app.schemas.post_schemas import PostsIn
from app.repositories.post_repos import create_post_repo, get_all_post_repo

def create_post_service(user_id, post: PostsIn):
        post_id = create_post_repo(user_id, post.title, post.content)
        if post_id is None:
            # will be change to a defined exception
            raise ValueError("Post not created")
        return post_id[0]

def get_all_post_service():
    posts = get_all_post_repo()
    if not posts:
        # will be change to a defined exception
        raise ValueError("Post does not exists")
    return posts

    

