from app.schemas.post_schemas import PostsIn
from app.repositories.post_repos import create_post_repo, get_all_post_repo, get_post_by_id_repo, get_post_by_title_repo

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

def get_post_by_id_service(post_id: str):
    post = get_post_by_id_repo(post_id)
    if post is None:
        raise ValueError("Post not found")
    return post

def get_post_by_title_service(title: str):
    post = get_post_by_title_repo(title)
    if post is None:
        raise ValueError("Post not found")
    return post

def delete_post_service(post_id):
    row = delete_post_repo(post_id)
    if row is None:
        raise ValueError("Not deleted")