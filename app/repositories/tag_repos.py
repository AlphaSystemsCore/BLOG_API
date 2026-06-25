from app.db.db_connection import get_cur

def save_tag_repo(user_id:str, tag_name:str, tag_category:str):
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO tags(tag_name, tag_category, user_id)
            VALUES(%s, %s, %s)
            """, (tag_name, tag_category, user_id)
        )

def delete_tag_repo(tag_id):
    with get_cur() as cur:
        cur.execute("DELETE FROM tags WHERE tag_id = %s", (tag_id,))

def get_tags_repo():
    with get_cur() as cur:
        cur.execute(
            "SELECT tag_id, tag_name, tag_category FROM tags"
        )