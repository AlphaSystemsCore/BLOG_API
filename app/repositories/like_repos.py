from app.db.db_connection import get_cur

def create_like_repo(user_id:str, post_id:str):
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO likes
            (user_id, post_id)
            VALUES(%s, %s) RETURINING like_id
            """, (user_id, post_id)
        )
        row = cur.fetchone()
    return row

# to reason about what to return and what inputs to take to delete like
def delete_like_repo(user_id, post_id):
    with get_cur() as cur:
        cur.execute(
            """
            DELETE FROM likes
            WHERE user_id = %s AND post_id = %s
            """, (user_id, post_id)
        )
        updated_row = cur.rowcount
    return updated_row

def get_total_like_count_repo(post_id):
    """counts likes per post"""
    with get_cur() as cur:
        cur.execute(
            """
            SELECT COUNT(*) FROM likes
            WHERE post_id = %s
            """,(post_id,)
        )
        total_likes = cur.fetchone()
    return total_likes