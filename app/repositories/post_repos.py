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
    # to add limit and offset (pagination)
    with get_cur() as cur:
        cur.execute(
            "SELECT p.post_id, p.title, p.content, p.created_at FROM posts p"
        )
        row = cur.fetchall()
    return row
    

def get_post_by_id_repo(post_id: str):
    with get_cur() as cur:
        cur.execute("""
        SELECT p.post_id, p.title, p.content, p.created_at 
            FROM posts p 
            WHERE p.post_id = %s""", (post_id,)
        )
        row = cur.fetchone()
    return row

def get_post_by_title_repo(title:str):
    with get_cur() as cur:
        cur.execute("""
        SELECT p.post_id, p.title, p.content, p.created_at 
            FROM posts p 
            WHERE p.title = %s""", (title,)
        )
        row = cur.fetchone()
    return row

def delete_post_repo(post_id:str):
    with get_cur() as cur:
        cur.execute(
            "DELETE FROM posts WHERE post_id = %s", (post_id,)
        )
        updated_rows = cur.rowcount
    return updated_rows