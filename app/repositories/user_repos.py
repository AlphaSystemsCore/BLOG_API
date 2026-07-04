from app.db.db_connection import get_cur

def get_user_profile_repo(user_id:str):
    with get_cur() as cur:
        cur.execute(
            """
            SELECT (username) FROM users
            WHERE user_id = %s
            """, (user_id,)
        )