from app.schemas.comment_schemas import CommentIn, CommentOut, ResponseComment, Pagination, ReplyIn
from app.repositories.comment_repos import create_comment_repo, delete_comment_repo, get_all_comments_repo, get_total_comment_count_repo
from app.exceptions.comment_exception import CommentOperationalError

from uuid import UUID
def create_comment_service(user_id, comment_in: CommentIn):
    """creates comment and return the created object"""
    create_comment_repo(user_id, comment_in.content_id, comment_in.content)
    pass

def get_comment_service(content_id:UUID, pagination: Pagination):
    """fetch comment using content_id"""
    pass

def update_comment(user_id:str, content_id: ContentIn):
    """modifies the created comment by user_id"""
    pass

def delete_comment_service(user_id:str, comment_id:str):
    """delete comment or reply since they both have user id this is dynamic"""
    pass

def create_reply(user_id: UUID, reply_in: Reply):
    """creates reply using the parent_comment_id to link reply to a comment"""
    pass

def get_replies_service(current_parent_comment_id:UUID):
    """fetch  reply or nested replies when parent_comment_id is given"""
    pass