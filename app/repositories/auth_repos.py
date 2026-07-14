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
        credential_id = cur.fetchone().get("credential_id")
        cur.execute(

            """
            INSERT INTO users
            (username, email, credential_id)
            VALUES(%s, %s, %s)
            RETURNING user_id
            """,(username, email, credential_id)
        )
        user_id = cur.fetchone().get("user_id")
        cur.execute(
            """
            INSERT INTO email_verification
            (hashed_email_verification_token, user_id, expire_at)
            VALUES(%s, %s, %s) 
            """,(hashed_evt, user_id, expire_at)
        )
    return user_id

def consume_token_repo(user_id:str, hashed_email_verification_token: str):
    with get_cur() as cur:
        cur.execute("""
            UPDATE email_verification
                SET status = 'used',
                    updated_at = NOW()
                WHERE user_id = %s AND hashed_email_verification_token = %s AND status='active' AND expire_at > NOW()
                RETURNING status
                """,(user_id, hashed_email_verification_token)
        )
        row = cur.fetchone()
        cur.execute(
            """
             UPDATE users
                SET is_verified = True, updated_at = NOW()
                WHERE user_id = %s
            """ ,(user_id,)
        )
    return row

def get_hashed_password_repo(email:str):
    with get_cur() as cur:
        cur.execute(
            """
            SELECT oc.hashed_password, u.user_id
                FROM users u
                JOIN oauth2_credential oc
                USING(credential_id)
            WHERE u.email = %s AND u.is_verified = true AND u.account_status = 'active'
            """, (email,)
        )
        row = cur.fetchone()
    return row

def save_refresh_token_repo(user_id, hashed_refresh_token, client, expire_at):
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO refresh_token
            (hashed_refresh_token, user_id, client, expire_at)
            VALUES(%s, %s, %s, %s) RETURNING refresh_token_id 
            """, (hashed_refresh_token, user_id, client, expire_at)
        )
        row = cur.fetchone()
    return row

def consume_refresh_token_repo(refresh_token_id, hashed_refresh_token):
    with get_cur() as cur:
        cur.execute(
            """
            UPDATE refresh_token
                SET is_revoked = True
                WHERE is_revoked = False AND refresh_token_id =%s AND hashed_refresh_token=%s 
                """, (refresh_token_id, hashed_refresh_token)
        )
        updated = cur.rowcount
    return updated > 0