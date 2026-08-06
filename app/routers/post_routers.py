from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse
from typing import Annotated, List
from uuid import UUID

from app.auth.jwt_handler import get_current_user
from app.services.post_service import *
from app.exceptions.post_exception import BlogException
from app.schemas.post_schemas import *



post_router = APIRouter(tags=["posts"])
from app.schemas.post_schemas import *


@post_router.post("/posts", response_model=PostOut)
def create_post(post_in: PostIn, user_id: Annotated[UUID, Depends(get_current_user)]):
    try:
        return create_post_service(user_id, post_in)
    except BlogException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@post_router.delete("/posts", response_model=FeedbackOut)
def delete_post(content_id: UUID, user_id: Annotated[UUID, Depends(get_current_user)]):
    try:
        return delete_post_service(user_id, content_id)
    except BlogException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@post_router.patch("/posts")
def update_post():
    pass

def get_filters(search):
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
            raise ValueError("Invalid filter")
        conditions.append(condition)
        parameters.append(v)
    return conditions, parameters

def create_sort(search):
    "this is a helper to extract field and create an order clause for sorting"
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
        raise ValueError(f"Invalid sort_by column{sort_by}")
    direction = sort_dict.sort.direction
    order_clause = f"ORDER BY {sort_column} {direction}"
    return order_clause
    

@post_router.get("/posts")
def get_posts(
    sort_options: SortOptions = Depends(),
    pagination: Pagination = Depends(),
    post_filters: PostFilters = Depends(),
    ):
    search = PostSearch(
        filters=post_filters,
        pagination=pagination,
        sort=sort_options
    )
    conditions, parameters = get_filters(search)
    return conditions, parameters

    
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