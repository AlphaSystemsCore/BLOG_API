from uuid import UUID
from app.schemas.post_schemas import PostSearch
from app.db.db_connection import get_cur

def create_post_repo(user_id: UUID, title: str, content: str) ->dict:
    """
    Creates the content the add, using the content_id it inserts post in the posts table
    """
    with get_cur() as cur:
        cur.execute(
            """
            INSERT INTO contents
            (type) VALUES ('post') RETURNING content_id
            """
        )
        row = cur.fetchone()
        content_id = row.get("content_id") if row else None

        if content_id is None:
            return None
        cur.execute(
            """
            INSERT INTO posts(user_id, content_id, title, content)
            VALUES(%s, %s, %s, %s) RETURNING content_id, title, content, status, created_at 
            """, (user_id, content_id, title, content)
        )
        row = cur.fetchone()
        if row is None:
            return None
    return row

def delete_post_repo(user_id:UUID, content_id: str):
    """
    deletes the post using the content_id and the user_id  post is flagged as delete for soft deletes.
    """
    with get_cur() as cur:
        cur.execute(
            """
            UPDATE posts
            SET status = 'deleted', deleted_at = NOW()
            WHERE content_id = %s AND user_id = %s
            """, (content_id, user_id)
        )
        row = cur.rowcount
    return row


def filters_helper(search):
    "helper, to create, sql filter, by dynamically creating the parameters and condition needed for filtering data"
    parameters = []
    conditions = []
    filters = search.filters.model_dump(exclude_none=True)
    column_map = {
        "author":"u.username = %s",
        "title":"p.title = %s",
        "content_id": "p.content_id = %s",
        "status": "p.status = %s",
        "created_after":"p.created_at >= %s",
        "created_before":"p.created_at <= %s",
    }

    for k, v in filters.items():
        condition = column_map.get(k)
        if condition is None:
            raise ValueError(f"Invalid filter field: {k} \nAllowed field fields are {','.join(column_map.keys())}")
        conditions.append(condition)
        parameters.append(v)
    return conditions, parameters

def sort_helper(search):
    "helper, to extract field and create an order clause for sorting"
    sort_map = {
        "title":"p.title",
        "created_at": "p.created_at",
        "likes":"likes",
        "author":"u.username",
        "comments": "comments",
        "replies":"replies"
    }
    sort_by = search.sort.by
    sort_column = sort_map.get(sort_by)
    if sort_column is None:
        raise ValueError(
        f"Invalid sort_field {sort_by}\nAllowed field are {', '.join(sort_map.keys())}"
        )
    direction = search.sort.direction.upper()
    order_clause = f"ORDER BY {sort_column} {direction} NULLS LAST"
    return order_clause

def pagination_helper(search):
    "helper, extract data from search and create a pagination the return the stringed OFFSET and LIMIT"
    limit = search.pagination.limit
    offset = search.pagination.offset
    return  f"LIMIT {limit} OFFSET {offset}"
