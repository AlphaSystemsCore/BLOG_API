from datetime import datetime
from app.db.db_connection import get_cur 

def get_email(email: str) -> None| tuple:
    with get_cur() as cur:
        cur.execute(
            "SELECT email FROM users WHERE email = %s ", (email,)
        )
        email  = cur.fetchone()
    return email

def register_user_repo(email:str, hashed_password: str, hashed_emvt:str, expire_at):
    with get_cur() as cur:

        cur.execute(
            """
            INSERT INTO oauth2_credential
            (hashed_password)
            VALUES(%s) RETURNING credential_id
            """, (hashed_password,)
            )
        credential_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO users
            (email, credential_id)
            VALUES(%s,%s) RETURNING user_id
            """, (email, credential_id)
        )
        user_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO email_verification
            (hashed_email_verification_token, user_id, expire_at)
            VALUES(%s, %s, %s)
            """, (hashed_emvt, user_id, expire_at)
        )
    return user_id

def get_hashed_password_user_id_repo(email: str):
    with get_cur() as cur:
        cur.execute(
            """
            SELECT oc.hashed_password, u.user_id, u.is_verified
                FROM users u
                JOIN oauth2_credential oc
                USING(credential_id)
                WHERE email = %s
            """,
            (email,)
        )
        row = cur.fetchone()
    return row

def save_refresh_token(
    user_id: str, 
    hashed_refresh_token: str, 
    client: str, 
    expire_at: datetime):
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO refresh_token
            (hashed_refresh_token, user_id, client, expire_at)
            VALUES(%s, %s, %s, %s) RETURNING refresh_token_id
            """,(hashed_refresh_token, user_id, client, expire_at)
        )
        refresh_token_id = cur.fetchone()
    return refresh_token_id

def get_email_verification_metadate_repo(user_id):
    with get_cur() as cur:
        cur.execute(
            """
            SELECT ev.hashed_email_verification_token ,ev.is_used, ev.expire_at, u.is_verified 
                FROM email_verification ev
                JOIN users u
                USING (user_id)
                WHERE user_id = %s
            """, (user_id,)
        )
        metadata = cur.fetchone()
    return metadata

def update_email_verification_repo(user_id: str, is_used: bool, updated_at:datetime, is_verified:str | None = None):
    with get_cur() as cur:
        cur.execute(
            """
            UPDATE email_verification
            SET 
                is_used = %s,
                updated_at = %s
            WHERE user_id = %s
            """,(is_used, updated_at, user_id)
        )
        cur.execute(
            """
            UPDATE users
            SET 
                is_verified = COALESCE(%s, is_verified)
            WHERE user_id =%s RETURNING is_verified
            """, (is_verified, user_id)
        )
        row = cur.fetchone()
    return row
