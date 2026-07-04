from app.db.db_connection import get_cur

def create_like_repo(user_id:str, post_id:str):
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO likes
            (user_id, post_id)
            VALUES(%s, %s)
            """, (user_id, post_id)
        )
        updated_row = cur.rowcount
    return updated_row