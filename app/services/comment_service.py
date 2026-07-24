from app.schemas.comment_schemas import CommentIn
from app.repositories.comment_repos import create_comment_repo, delete_comment_repo, get_all_comments_repo, get_total_comment_count_repo
from app.exceptions.comment_exception import CommentOperationalError

# will declare a defined exception later
def create_comment_service(user_id, comment_in: CommentIn):
    """creates comments using the CommentIn model, in comment schemas """
    comment_id = create_comment_repo(user_id, comment_in.content_id, content_in.content)
    if comment_id is None:
        raise ValueError("Error occured comment not created")
    return comment_id
    
def delete_comment_service(user_id:str, comment_id: str):
    """deletes comment by specific user"""
    updated_rows = delete_comment_repo(user_id, comment_id)
    if not updated_rows:
        raise ValueError("Error occured comment not deleted")
    return {"status":"deleted successfully."}

def get_all_comments_service(post_id):
    """gets all comment for a particular post"""
    comments = get_all_comments_repo(post_id)
    if not comments:
        return []
    return comments

def get_total_comment_count_service(post_id: str):
    """counts all comment for each post and returns the total"""
    total_comments = get_total_comment_count_repo(post_id)
    return {"total_comments": total_comments}