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
            (hashed_token, user_id, expire_at)
            VALUES(%s, %s, %s)
            """, (hashed_emvt, user_id, expire_at)
        )
    return user_id

def get_hashed_password_user_id_repo(email: str):
    with get_cur() as cur:
        cur.execute(
            """
            SELECT oc.hashed_password, u.user_id
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

def get_email_verification_token_service(user_id):
   pass