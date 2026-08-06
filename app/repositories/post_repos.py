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
    order_clause = f" ORDER BY {sort_column} {direction} NULLS LAST "
    return order_clause

def pagination_helper(search):
    "helper, extract data from search and create a pagination the return the stringed OFFSET and LIMIT"
    pagination_clause = []
    limit = search.pagination.limit
    offset = search.pagination.offset
    pagination_clause = f" LIMIT %s OFFSET %s "
    parameters = [limit, offset]
    return pagination_clause, parameters

def sql_assembler(search):
    base_query = """
        SELECT 
            p.content_id, 
            p.title, 
            p.content, 
            u.username as author, 
            p.status,
            p.created_at, 
            COUNT( DISTINCT l.like_id) as likes, 
            COUNT(DISTINCT cm.comment_id) AS comments, 
            COUNT(DISTINCT cm.parent_comment_id) as replies
        FROM posts p
        JOIN users u
            ON u.user_id = p.user_id
        LEFT JOIN comments cm
            ON p.content_id = cm.content_id
        LEFT JOIN likes l
            ON p.content_id = l.content_id
        WHERE 
            u.is_verified = True 
            AND p.is_allowed = True 
            AND p.status = 'drafted' 
            AND p.deleted_at IS NULL 
            AND cm.deleted_at IS NULL 
        """
    conditions, parameters = filters_helper(search)
    order_by_clause = sort_helper(search)
    pagination_clause, pagination_params = pagination_helper(search)
    parameters += pagination_params

    group_by_clause = " GROUP BY p.content_id, p.title, p.content, u.username, p.status, p.created_at "
    if not conditions:
        dynamic_sql = base_query + group_by_clause + order_by_clause + pagination_clause
        return dynamic_sql, parameters

    dynamic_sql = base_query
    dynamic_sql+=' AND ' + ' AND '.join(conditions)
    dynamic_sql+=group_by_clause
    dynamic_sql+=order_by_clause
    dynamic_sql+=pagination_clause

    return dynamic_sql, parameters

def get_posts_repo(search):
    sql, parameters = sql_assembler(search)
    with get_cur() as cur:
        cur.execute(
            sql, parameters

        )
        row = cur.fetchall()
    return row
