from uuid import UUID

from app.schemas.post_schemas import *
from app.exceptions.post_exception import *
from app.repositories.post_repos import *

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

    
def get_posts_service():
    """multifunctional gets post, by the given query or by default returns posts with no constraint apart from pagination"""
    posts = [PostOut(**post) for post in get_posts_repo()]
    return posts
    
    
    
    
    # params = []
    # if search_constraints.author != None:
    #     condition += "username = %s "
    #     params.append(search_constraints.author)
    # if search_constraints.content_id != None:
    #     condition += "content_id = %s "
    #     params.append(search_constraints.content_id)
    # if search_constraints.title != None:
    #     condition += "title = %s "
    #     params.append(search_constraints.title)

    # query = "SELECT * FROM posts"
    # if condition:
    #     query += "WHERE" += "AND".join(condition)
    
    # get_posts_repo(query, params)