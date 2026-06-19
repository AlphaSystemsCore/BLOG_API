from app.db.db_connection import get_cur 

def get_email(email: str) -> None| tuple:
    with get_cur() as cur:
        cur.execute(
            "SELECT email FROM users WHERE email = %s ", (email,)
        )
        email  = cur.fetchone()
    return email

def register_user_repo(email:str, hashed_password: str, hashed_emvt:str):
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
            (hashed_token, user_id)
            VALUES(%s, %s)
            """, (hashed_emvt, user_id)
        )


