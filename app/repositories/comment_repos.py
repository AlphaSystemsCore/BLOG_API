from app.db.db_connection import get_cur

def create_comment_repo(user_id:str, content_id:str, content:str):
    """creates the content, the use the content_id to link the comment"""
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO comments
            (content, content_id, user_id)
            VALUES(%s,%s, %s) RETURNING comment_id, content, created_at
            """, (content, content_id, user_id)
        )
        row = cur.fetchone()
    return row
    
def delete_comment_repo(user_id:str, comment_id: str):
    """deletes the comment using user_id"""
    with get_cur() as cur:
        cur.execute(
            """
            DELETE FROM comments
            WHERE user_id = %s AND content_id = %s
            """, (user_id, content_id)
        )
        updated_row = cur.rowcount
    return updated_row


def get_comments_repo(post_id:str, limit: int, offset: int):
    """get comments """

