from app.db.db_connection import get_cur

def create_comment_repo(user_id:str, content:str):
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO contents(type)
            VALUES('comment') RETURNING content_id
            """
        )
        content_id = cur.fetchone()
        if content_id is None:
            return None
        cur.execute(
            """
            INSERT INTO comments
            (content, content_id, user_id)
            VALUES(%s,%s, %s) RETURNING content_id, content, created_at
            """, (content, content_id, user_id)
        )
        row = cur.fetchone()
    return row
    
def delete_comment_repo(user_id:str, comment_id: str):
    with get_cur() as cur:
        cur.execute(
            """
            DELETE FROM comments
            WHERE user_id = %s AND comment_id = %s
            """, (user_id, comment_id)
        )
        updated_rows = cur.rowcount
    return updated_rows

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
