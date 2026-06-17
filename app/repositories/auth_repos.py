from app.db.db_connection import get_cur 

def get_email(email: str) -> None| tuple:
    with get_cur() as cur:
        cur.execute(
            "SELECT email FROM users WHERE email = %s ", (email,)
        )
        email  = cur.fetchone()
    return email

def create_user(emaiL:str, hashed_password: str):
    pass