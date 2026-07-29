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


def get_comments_repo(content_id:UUID, limit:int, offset:int):
    """
    fetch comment using content_id
    cm comment
    ccm child comment
    """
    with get_cur() as cur:
        cur.execute(
            """
            SELECT cm.comment_id, u.username as author, cm.content, COUNT(DISTINCT ccm.comment_id) as replies, created_at
            FROM comments c
            LEFT JOIN users u
            USING(user_id)
            JOIN comments ccm
            ON c.comment_id = ccm.parent_comment_id
            WHERE content_id = %s , parent_comment_id IS NULL AND deleted_at is NOT NULL
            GROUP BY cm.comment_id, author, content, created_at
            ORDER BY cm.created_at DESC
            """, (content_id, limit, offset)
        )
        row = cur.fetchall()

    return row

def update_comment_repo(user_id:UUID, comment_id:UUID, content:str):
    with get_cur() as cur:
        cur.execute(
            """
            UPDATE comments
                SET content = %s, updated_at = NOW()
            WHERE user_id = %s AND comment_id = %s
            """, (content, user_id, comment_id)
        )
        row = cur.rowcount
    return row


def delete_comment_repo(user_id:UUID, comment_id:UUID):
    with get_cur() as cur:
        cur.execute(
            """
            DELETE FROM comments
                WHERE user_id = %s AND comment_id = %s
            """, (user_id, comment_id)
        )
        row = rowcount
    return row

def create_reply_repo(user_id:UUID, parent_comment_id:UUID, content:str):
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO comments
            (user_id, parent_comment_id, content)
            VALUES(%s, %s, %s) RETURNING parent_comment_id, comment_id, content, created_at
            """, (user_id, parent_comment_id, content)
        )
        row = fetchone()
    return row

def get_replies_repo(current_parent_comment_id:UUID):
    with get_cur() as cur:
        cur.execute(
            """
            SELECT 
                r.parent_comment_id, 
                r.comment_id, 
                u.username as author, 
                r.content, 
                COUNT(cr.comment_id) as replies, 
                r.created_at
            FROM comments r
                JOIN users u
            USING(user_id)
                JOIN comments as cr
            ON r.comment_id = cr.parent_comment_id
            WHERE 
                r.parent_comment_id = %s 
                AND r.parent_comment_id IS NOT NULL 
                AND r.deleted_at IS NOT NULL
            GROUP BY r.parent_commit_id, r.comment_id, u.username, r.content, r.created_at
            ORDER BY r.created_at DESC
            LIMIT %s 
            OFFSET %s

            """, (current_parent_comment_id,  limit, offset)
        )
        row = cur.fetchall()
    return row



    

