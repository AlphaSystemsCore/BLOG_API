from uuid import UUID

from app.db.db_connection import get_cur

def create_post_repo(user_id: UUID, title: str, content: str) ->dict:
    """
    Creates the content the add, using the content_id it inserts post in the posts table
    """
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO contents
            (type) VALUES ('post') RETURNING content_id
            """
        )
        row = cur.fetchone()
        content_id = row.get("content_id") if row else None

        if content_id is None:
            return None
        cur.execute(
            """
            INSERT INTO posts(user_id, content_id, title, content)
            VALUES(%s, %s, %s, %s) RETURNING content_id, title, content, status, created_at 
            """, (user_id, content_id, title, content)
        )
        row = cur.fetchone()
        if row is None:
            return None
    return row

def delete_post_repo(user_id:UUID, content_id: str):
    """
    deletes the post using the content_id and the user_id  post is flagged as delete for soft deletes.
    """
    with get_cur() as cur:
        cur.execute(
            """
            UPDATE posts
            SET status = 'deleted', deleted_at = NOW()
            WHERE content_id = %s AND user_id = %s
            """, (content_id, user_id)
        )
        row = cur.rowcount
    return row

