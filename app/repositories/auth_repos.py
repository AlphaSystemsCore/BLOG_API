from datetime import datetime
from app.db.db_connection import get_cur


def register_user_save_evt(username: str, email: str, hashed_password: str, hashed_evt: str, expire_at: datetime):
    # evt is email_verification_token 
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO oauth2_credential(hashed_password)
            VALUES(%s) RETURNING credential_id
            """, (hashed_password,)
        )
        credential_id = cur.fetchone()[0]
        print(credential_id)
        cur.execute(

            """
            INSERT INTO users
            (username, email, credential_id)
            VALUES(%s, %s, %s)
            RETURNING user_id
            """,(username, email, credential_id)
        )
        user_id = cur.fetchone()[0]
        print(user_id)
        cur.execute(
            """
            INSERT INTO email_verification
            (hashed_email_verification_token, user_id, expire_at)
            VALUES(%s, %s, %s)
            """,(hashed_evt, user_id, expire_at)
        )