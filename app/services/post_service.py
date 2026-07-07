from app.schemas.post_schemas import PostIn, PostOut
from app.repositories.post_repos import create_post_repo, get_all_post_repo, get_post_by_id_repo, get_post_by_title_repo, delete_post_repo
from app.exceptions.post_exception import *



def get_all_post_service():
    """returns a list of dictionary"""
    posts = get_all_post_repo()
    if not posts:
        return []
    post_list =[]
    for p in posts:
        post_dict = {
            "post_id":p[0],
            "title":p[1],
            "content":p[2],
            "created_at":p[3]
        }
        post_list.append(post_dict)
    return post_list


def get_post_by_id_service(post_id: str):
    """return a dictionary of post using the PostOut schema"""
    post = get_post_by_id_repo(post_id)
    if post is None:
        raise PostNotFoundError(f"Post not found: {post_id}")
    return {
            "post_id":post[0],
            "title":post[1],
            "content":post[2],
            "created_at":post[3]
        }

def get_post_by_title_service(title: str):
    """Gets the post by it's title"""
    post = get_post_by_title_repo(title)
    if post is None:
        raise PostNotFoundError("Post not found: {title}")
    return {
            "post_id":post[0],
            "title":post[1],
            "content":post[2],
            "created_at":post[3]
        }

# user restricted action
def create_post_service(user_id, post_in: PostIn):
    """Creates the post using the PostIn schema in post_schemas"""
    post_id = create_post_repo(user_id, post_in.title, post_in.content)
    if post_id is None:
        raise FailedToCreatePostError("Failed to create post: post_id.title")
    return {
        "post_id": post_id,
        "status": "created",
    }

def delete_post_service(user_id, post_id):
    """Deletes the post by post_id and user_id who created the post"""
    updated_rows = delete_post_repo(user_id, post_id)
    if not updated_rows:
        raise DeletionFailedError("Failed to delete post: {post_id}".format(post_id))
    return {
        "post_id":post_id,
        "status":"deleted"
    }

def update_post(user_id, post_update:PostUpdate):
    # to be implemented
    pass

def publish_post_service(user_id:str, post_id:str):
    row_updated = publish_post_repo
    if not row_updated:
        raise PublishPostFailedError(f"Failed to publish this post: {post_id}")
    return {
        "post_id":post_id,
        "status": "published"
    } 
