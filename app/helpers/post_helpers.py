from app.exceptions.post_exception import PostOperationError
def filters_helper(search):
    """
    helper, to create, sql filter, by dynamically creating the parameters and condition needed for filtering data
    """
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
            raise PostOperationError(f"Invalid filter field: {k}\nAllowed fields or columns are {','.join(column_map.keys())}")
        conditions.append(condition)
        parameters.append(v)
    return conditions, parameters

def sort_helper(search):
    """
    helper, to extract field and create an order clause for sorting
    """
    parameters = []
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
        raise PostOperationError(
        f"Invalid sort field; You entered this: {sort_by}\nAllowed field are {', '.join(sort_map.keys())}"
        )
    direction = search.sort.direction.upper()

    order_clause = f" ORDER BY {sort_column} {direction} NULLS LAST "
    return order_clause

def pagination_helper(search):
    """
    helper, extract data from search and create a pagination the return the stringed OFFSET and LIMIT
    """
    pagination_clause = []
    limit = search.pagination.limit
    offset = search.pagination.offset
    pagination_clause = f" LIMIT %s OFFSET %s "
    parameters = [limit, offset]
    return pagination_clause, parameters