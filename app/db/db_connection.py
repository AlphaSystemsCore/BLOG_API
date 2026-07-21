import psycopg2 
from psycopg2.pool  import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import logging

from app.core.load_envs import DATABASE_URL

db_pool = psycopg2.pool.SimpleConnectionPool(
    1,
    20,
    host="localhost",
    database="blog",
    user="postgres",
    password="@create2026",
    port=5432,
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
        cur = conn.cursor(cursor_factory=RealDictCursor)   
        try:
            yield cur
            conn.commit()
        except Exception as e:
            
            conn.rollback()
            raise
        finally:
            cur.close()

from app.models.tables import blog_api_table_production
if __name__ == "__main__":
    with get_cur() as cur:
        count = 0
        for table in blog_api_table_production:
            cur.execute(table)
            print("Inserting table....")
            count +=1
            print(count)

