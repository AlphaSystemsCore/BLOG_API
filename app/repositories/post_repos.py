from app.db.db_connection import get_cur

def create_post_repo(user_id:str, title: str, content:str ):
    """Creates the post using title, content and user_id"""
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO posts 
                (user_id, title, content)
                VALUES(%s, %s, %s) RETURNING post_id, user_id, title, content
            """, (user_id, title, content)
        )
        post = cur.fetchone()
    return post
# to implement pagination on this
def get_all_post_repo(): 
    """Returns all posts that are published """
    with get_cur() as cur:
        cur.execute(
            """
            SELECT
                p.post_id, u.username,  p.title, p.content, p.created_at 
            FROM posts p
            JOIN user u
            USING(post_id)
            WHERE p.is_allowed = true AND p.status = 'published'
            """
        )
        post = cur.fetchall()
    return post
    
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

def delete_post_repo(user_id:str, post_id:str):
    with get_cur() as cur:
        cur.execute(
            "DELETE FROM posts WHERE user_id = %s AND post_id = %s", (user_id, post_id,)
        )
        updated_rows = cur.rowcount
    return updated_rows


def publish_post_repo(user_id, post_id):
    with get_cur() as cur:
        cur.execute(
            """
            UPDATE posts
            SET status = 'published' , updated_at = NOW()
            WHERE user_id = %s AND post_id = %s
            """, (user_id, post_id)
        )