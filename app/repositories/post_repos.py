from app.db.db_connection import get_cur

def create_post_repo(user_id:str, title: str, content:str ):
    """ 
    Creates the post using title, content and user_id,
    the next version must include media for posts
    """
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO posts 
                (user_id, title, content)
                VALUES(%s, %s, %s) RETURNING post_id, title, content, created_at
            """, (user_id, title, content)
        )
        post = cur.fetchone()
    return post

# to implement pagination on this
# to change the status to published later
def get_all_post_repo(): 
    """Returns all posts that are published """
    with get_cur() as cur:
        cur.execute(
            """
            SELECT
                p.post_id, u.username AS author, p.title, p.content, COUNT(l.post_id) AS likes, COUNT(c.post_id) AS comments, p.created_at 
            FROM posts p
            LEFT JOIN users u
            ON p.user_id = u.user_id
            LEFT JOIN likes l
            ON l.post_id = p.post_id
            LEFT JOIN comments c
            ON c.post_id = p.post_id
            WHERE p.status = 'drafted' AND p.is_allowed = true
            GROUP BY p.post_id, u.username, p.title, p.content, p.created_at
            """
        )
        post = cur.fetchall()
        print(post)
    return post
    
def get_post_by_id_repo(post_id: str):
    with get_cur() as cur:
        cur.execute(
            """
            SELECT
                p.post_id, u.username AS author, p.title, p.content, COUNT(l.post_id) AS likes, COUNT(c.post_id) AS comments, p.created_at 
            FROM posts p
            LEFT JOIN users u
                ON p.user_id = u.user_id
            LEFT JOIN likes l
                ON l.post_id = p.post_id
            LEFT JOIN comments c
                ON c.post_id = p.post_id
            WHERE p.status = 'published' AND p.is_allowed = true AND p.post_id = %s
            GROUP BY p.post_id, u.username, p.title, p.content, p.created_at
            """,(post_id,)
        )
        post = cur.fetchone()
    return post

def get_post_by_title_repo(title:str):
    """Fetch's the post by its title"""
    with get_cur() as cur:
        cur.execute(
            """
            SELECT
                p.post_id, u.username AS author, p.title, p.content, COUNT(l.post_id) AS likes, COUNT(c.post_id) AS comments, p.created_at 
            FROM posts p
            LEFT JOIN users u
            ON p.user_id = u.user_id
            LEFT JOIN likes l
            ON l.post_id = p.post_id
            LEFT JOIN comments c
            ON c.post_id = p.post_id
            WHERE p.status = 'drafted' AND p.is_allowed = true AND p.title = %s
            GROUP BY p.post_id, u.username, p.title, p.content, p.created_at
            """,(title,)
        )
        post = cur.fetchone()
    return post

def get_posts_by_author(username):
    """Get post by Author"""
    with get_cur() as cur:
        cur.execute(
            """
            SELECT
                p.post_id, u.username AS author, p.title, p.content, COUNT(l.post_id) AS likes, COUNT(c.post_id) AS comments, p.created_at 
            FROM posts p
            LEFT JOIN users u
            ON p.user_id = u.user_id
            LEFT JOIN likes l
            ON l.post_id = p.post_id
            LEFT JOIN comments c
            ON c.post_id = p.post_id
            WHERE p.status = 'drafted' AND p.is_allowed = true AND u.username = %s
            GROUP BY p.post_id, u.username, p.title, p.content, p.created_at
            """,(username,)
        )
        post = cur.fetchall()
    return post

def delete_post_repo(user_id:str, post_id:str):
    """Deletes a post from using user_id and post_id"""
    with get_cur() as cur:
        cur.execute(
            "DELETE FROM posts WHERE user_id = %s AND post_id = %s", (user_id, post_id,)
        )
        updated_row = cur.rowcount
    return updated_row


def publish_post_repo(user_id:str, post_id:str):
    """making the post available to the public"""
    with get_cur() as cur:
        cur.execute(
            """
            UPDATE posts
            SET status = 'published', updated_at = NOW()
            WHERE user_id = %s AND post_id = %s AND status <> 'published' RERURNING status
            """, (user_id, post_id)
            )
        status = cur.fetchone()
    return status

def update_post_repo(user_id:str, post_id:str, title: str | None, content:str| None):
    """to update post using tiltle and content"""
    with get_cur() as cur:
        cur.execute(
            """
            UPDATE posts 
            SET title = COALECSE(%s, title)
                content = COALECSE(%s, content)
            WHERE user_id = %s AND post_id = %s RETURNING post_id, title, content
            """, (title, content, user_id, post_id)
        )
        post = cur.fetchone()
    return post