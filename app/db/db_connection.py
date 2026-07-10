import psycopg2 
from psycopg2.pool  import SimpleConnectionPool
from contextlib import contextmanager
import logging


db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn = 20,
    **config
)

@contextmanager
def get_conn():
    conn = db_pool.getconn()
    try:
        yield conn
    except Exception as e:
        print("Error: ",e)
        raise
    finally:
        db_pool.putconn(conn)

@contextmanager
def get_cur():
    with get_conn() as conn:
        cur = conn.cursor()
        try:
            yield cur
            conn.commit()
        except Exception as e:
            
            conn.rollback()
            raise
        finally:
            cur.close()

from app.models.tables import blog_api_table_preliminary
if __name__ == "__main__":
    with get_cur() as cur:
        count = 0
        for table in blog_api_table_preliminary:
            cur.execute(table)
            print("Inserting table....")
            count +=1
            print(count)