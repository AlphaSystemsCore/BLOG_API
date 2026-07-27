from app.db.db_connection import get_cur

def create_comment_repo(user_id:str, content:str):
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO contents(type)
            VALUES('comment') RETURNING content_id
            """
        )
        row = cur.fetchone()
        content_id = row if row is not None else None
        if content_id == None:
            return False
        cur.execute(
            """
            INSERT INTO comments
            (content, content_id, user_id)
            VALUES(%s,%s, %s) RETURNING content_id, comment_id, content, created_at
            """, (content, content_id, user_id)
        )
        row = cur.fetchone()
    return row
    
def delete_comment_repo(user_id:str, comment_id: str):
    with get_cur() as cur:
        cur.execute(
            """
            DELETE FROM comments
            WHERE user_id = %s AND content_id = %s
            """, (user_id, content_id)
        )
        updated_row = cur.rowcount
    return updated_row

def get_all_comments_repo(post_id:str):
    with get_cur() as cur: 
        cur.execute(
            """
            SELECT c.content, c.post_id, c.user_id 
            FROM comments c 
            WHERE post_id = %s """, (post_id,)
        )
        row = cur.fetchall()
    return row

def get_total_comment_count_repo(post_id:str):
    with get_cur() as cur:
        cur.execute(
            """
            SELECT COUNT(*) FROM comments WHERE post_id = %s
            """, (post_id,)
        )
        comment_count = cur.fetchone()
    return comment_count
