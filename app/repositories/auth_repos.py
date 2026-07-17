from datetime import datetime
from app.db.db_connection import get_cur


def register_user_save_evt_repo(username: str, email: str, hashed_password: str, hashed_evt: str, expire_at: datetime):
    """
    evt is email_verification_token
    This repo creates new user
    """
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO oauth2_credential(hashed_password)
            VALUES(%s) RETURNING credential_id
            """, (hashed_password,)
        )
        credential_id = cur.fetchone().get("credential_id")
        if credential_id is None:
            return None
        cur.execute(

            """
            INSERT INTO users
            (username, email, credential_id)
            VALUES(%s, %s, %s)
            RETURNING user_id
            """,(username, email, credential_id)
        )
        user_id = cur.fetchone().get("user_id")
        if user_id is None:
            return None
        cur.execute(
            """
            INSERT INTO email_verification
            (hashed_email_verification_token, user_id, expire_at)
            VALUES(%s, %s, %s) 
            """,(hashed_evt, user_id, expire_at)
        )
    return user_id

def consume_token_repo(user_id: str, hashed_email_verification_token: str):
    """
    flags token as used,
    marks user as verified
    """
    with get_cur() as cur:
        # Expire old tokens
        cur.execute(
            """
            UPDATE email_verification
                SET status = 'expired'
            WHERE expire_at < NOW() AND user_id = %s AND hashed_email_verification_token = %s
            RETURNING status
            """, (user_id, hashed_email_verification_token)
        )
        status_row = cur.fetchone()
        if status_row is not None:
            return status_row.get("status")

        # Consume active token
        cur.execute(
            """
            UPDATE email_verification
                SET status = 'used',
                    updated_at = NOW()
                WHERE 
                    user_id = %s AND 
                    hashed_email_verification_token = %s AND 
                    status = 'active'
                RETURNING status
            """,
            (user_id, hashed_email_verification_token)
        )
        status_row = cur.fetchone()
        status = status_row.get("status") if status_row else None
        if status is None:
            return "invalid"

        # Mark user verified
        cur.execute(
            """
            UPDATE users
                SET is_verified = TRUE, updated_at = NOW()
                WHERE user_id = %s 
                RETURNING user_id
            """,
            (user_id,)
        )
        user_row = cur.fetchone()
        user_id = user_row.get("user_id") if user_row else None

    return user_id


def get_hashed_password_repo(email:str):
    """gets hashed password, if account is active and verified"""
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

def save_refresh_token_repo(user_id:str, hashed_refresh_token:str, client:str, expire_at:datetime):
    """stores refresh token in the"""
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

def consume_refresh_token_repo(refresh_token_id:str, hashed_refresh_token:str):
    """flags refresh token as revoked to avoid double usage"""
    with get_cur() as cur:
        cur.execute(
            """
            UPDATE refresh_token
                SET is_revoked = True
                WHERE is_revoked = False AND refresh_token_id =%s AND hashed_refresh_token=%s AND expire_at < NOW()
                """, (refresh_token_id, hashed_refresh_token)
        )
        is_revoked = cur.fetchone()
        is_revoked = is_revoked.get("is_revoked") if is_revoked else None
    return is_revoked

def create_new_email_verification_token_repo(email:str, hashed_evt:str, expire_at: datetime):
    """lookup for user only who is not verified, revoke the token then create new token"""
    with get_cur() as cur:
        cur.execute(
            """
            SELECT user_id FROM users 
            WHERE email = %s AND is_verified = false
            """,(email,)
        )
        row = cur.fetchone()
        user_id = row.get("user_id") if row else None
        if user_id is None:
            return None
        cur.execute(
            """
            UPDATE email_verification
                SET status = 'revoked', updated_at = NOW()
            WHERE user_id =%s and status = 'active'
            """, (user_id,)
        )
        cur.execute(
            """
            INSERT INTO email_verification
            (hashed_email_verification_token, user_id, expire_at )
            VALUES(%s, %s, %s) 
            """,(hashed_evt, user_id, expire_at)
        )
    return user_id