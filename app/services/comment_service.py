from app.schemas.comment_schemas import CommentIn, CommentOut, ResponseComment, Pagination, ReplyIn,ReplyOut, ContentToUpdate
from app.repositories.comment_repos import (
    create_comment_repo, 
    delete_comment_repo, 
    get_comments_repo,
    update_comment_repo,
    create_reply_repo,
    get_replies_repo, 
    )
from app.exceptions.comment_exception import CommentOperationalError

from uuid import UUID
def create_comment_service(user_id, comment_in: CommentIn):
    """creates comment and return the created object"""
    comment = create_comment_repo(user_id, comment_in.content_id, comment_in.content)
    if comment is None:
        raise CommentOperationalError("Failed to create comment, please try again")
    return comment

def get_comments_service(content_id:UUID, pagination: Pagination):
    """fetch comment using content_id"""
    rows = get_comments_repo(content_id, pagination.limit, pagination.offset)
    if not rows:
        raise CommentOperationalError("No comments")
    comments = [CommentOut(**comment)for comment in rows]
    return comments

def update_comment(user_id:str, content_to_update:ContentToUpdate):
    """modifies the created comment by user_id"""
    row_count = update_comment_repo(user_id, content_to_update.comment_id, content_to_update.content)
    if row_count == 0:
        raise CommentOperationalError(f"Failed to update comment, please try again")
    return ResponseComment(comment_id=content_to_update.comment_id, message="updated successfully")
    

def delete_comment_service(user_id:str, comment_id:str):
    """delete comment or reply since they both have user id this is dynamic"""
    row_count = delete_comment_repo(user_id, comment_id)
    if row_count == 0:
        raise CommentOperationalError(f"Failed to delete comment, please try again")
    return ResponseComment(comment_id=comment_id, message="comment ")

def create_reply(user_id: UUID, reply_in: ReplyIn):
    """creates reply using the parent_comment_id to link reply to a comment"""
    row = create_reply_repo(user_id, reply_in.current_parent_comment_id, reply_in.content)
    if row is None:
        raise CommentOperationalError("Failed to create reply, please try again")
    return ReplyOut(**row)
    

def get_replies_service(current_parent_comment_id:UUID):
    """fetch  reply or nested replies when parent_comment_id is given"""
    row = get_replies_repo(current_parent_comment_id)
    if row is None:
        raise CommentOperationalError("No replies found")
    replies = [ReplyOut(**reply) for reply in row]
    return replies