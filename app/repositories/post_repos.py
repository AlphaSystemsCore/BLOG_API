from app.db.db_connection import get_cur

def create_post_repo(user_id:str, title: str, content:str, image_link: str | None, video_link: str | None, status: str ):
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO posts 
                (user_id, title, content, image_link, video_link, status)
                VALUES(%s, %s, %s, COALESE(%s, image_link), COALESE(%s, video_link), %s)
            """, (user_id, title, content, image_link, video_link, status)
        )

    