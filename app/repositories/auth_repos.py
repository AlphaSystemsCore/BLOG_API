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
        cur.execute(

            """
            INSERT INTO users
            (username, email, credential_id)
            VALUES(%s, %s, %s)
            RETURNING user_id
            """,(username, email, credential_id)
        )
        user_id = cur.fetchone()[0]
        cur.execute(
            """
            INSERT INTO email_verification
            (hashed_email_verification_token, user_id, expire_at)
            VALUES(%s, %s, %s) 
            """,(hashed_evt, user_id, expire_at)
        )
    return user_id
    
def update_email_verification_token_repo(user_id:str, token_id: str):
    with get_cur() as cur:
        cur.execute("""
            UPDATE email_verification
                SET status = 'used',
                    updated_at = NOW()
                WHERE user_id = %s AND token_id = %s AND status='active' AND expire_at > NOW()
                RETURNING hashed_email_verification_token, expire_at, status
                """,(user_id, token_id)
        )