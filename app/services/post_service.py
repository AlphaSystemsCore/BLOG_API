from app.schemas.post_schemas import PostsIn
from app.repositories.post_repos import create_post_repo, get_all_post_repo, get_post_by_id_repo, get_post_by_title_repo, delete_post_repo


class PostNotFoundError(Exception):
    pass
class FailedToCreatePostError(Exception):
    pass

def get_all_post_service():
    """Returns all posts, return a tuple of posts"""
    posts = get_all_post_repo()
    if not posts:
        return []
    return posts

def get_post_by_id_service(post_id: str):
    """Gets post by post_id"""
    post = get_post_by_id_repo(post_id)
    if post is None:
        raise PostNotFoundError("Post not found")
    return post

def get_post_by_title_service(title: str):
    """Gets the post by it's title"""
    post = get_post_by_title_repo(title)
    if post is None:
        raise PostNotFoundError("Post not found")
    return post

# user defined actions in posts
def create_post_service(user_id, post: PostsIn):
    """Creates the post using the PostIn schema in post_schemas"""
    post_id = create_post_repo(user_id, post.title, post.content)
    if post_id is None:
        raise FailedToCreatePostError("Failed to create post")
    return post_id[0]

def delete_post_service(user_id, post_id):
    """Deletes the post by id post_id and user_id who created the post"""
    updated_rows = delete_post_repo(user_id, post_id)
    if not updated_rows:
        # will be change to a defined exception
        raise ValueError("Not deleted")
    return {"deleted":"successfully"}