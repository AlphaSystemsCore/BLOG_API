from app.db.db_connection import get_cur
from uuid import UUID

def create_comment_repo(user_id:UUID, content_id:UUID, content:str):
    """creates comment and return the created object"""
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO comments
            (user_id, content_id, content)
            VALUES(%s, %s, %s) RETURINING comment_id, content, created_at
            """
        )
        row = cur.fetchone()


def get_comment_repo(content_id:UUID, limit:int, offset:int):
    """
    fetch comment using content_id
    cm comment
    ccm child comment
    """
    with get_cur() as cur:
        cur.execute(
            """
            SELECT cm.comment_id, u.username as author, cm.content, COUNT(DISTINCT ccm.parent_comment_id) as replies, created_at
            FROM comments c
            LEFT JOIN users u
            USING(user_id)
            JOIN comments ccm
            ON c.comment_id = ccm.parent_comment_id
            GROUP BY cm.comment_id, author, content, created_at
            ORDER BY cm.created_at DESC
            """
        )
        row = cur.fetchall()

    return row

def

    

