from app.db.db_connection import get_cur
from uuid import UUID

def save_tag_repo(user_id:UUID, tag_name:str, tag_category:str):
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO tags(tag_name, tag_category, user_id)
            VALUES(%s, %s, %s), RETURNING tag_id, tag_name, tag_category
            """, (tag_name, tag_category, user_id)
        )
        row = fetchone()
    return row

def delete_tag_repo(tag_id:UUID):
    """deletes only when user is authorised a tag  and tag_Id"""
    with get_cur() as cur:
        cur.execute("DELETE FROM tags WHERE tag_id = %s", (tag_id,))
        row = cur.rowcount
    return row


def get_tags_repo():
    """get all tags no pagination, pagination will be implemented soon"""
    with get_cur() as cur:
        cur.execute(
            "SELECT tag_id, tag_name, tag_category FROM tags"
        )
        rows = cur.fetchall()
    return rows