from app.db.db_connection import get_cur

def create_post_repo(user_id:str, title: str, content:str ):
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO posts 
                (user_id, title, content)
                VALUES(%s, %s, %s) RETURNING post_id
            """, (user_id, title, content)
        )
        row = cur.fetchone()
    return row

def get_all_post_repo():
    with get_cur() as cur:
        cur.execute(
            "SELECT p.post_id, p.title, p.content, p.created_at FROM posts p"
        )
        row = cur.fetchall()
    return row
    