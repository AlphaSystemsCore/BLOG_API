from app.db.db_connection import get_cur 

def get_email(email: str) -> None| tuple:
    with get_cur() as cur:
        cur.execute(
            "SELECT email"
        )