from app.schemas.post_schemas import PostsIn, PostOut
from app.repositories.post_repos import create_post_repo, get_all_post_repo, get_post_by_id_repo, get_post_by_title_repo, delete_post_repo


class PostNotFoundError(Exception):
    pass
class FailedToCreatePostError(Exception):
    pass



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
        return []
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
        raise PostNotFoundError("Post not found")
    return {
            "post_id":post[0],
            "title":post[1],
            "content":post[2],
            "created_at":post[3]
        }

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