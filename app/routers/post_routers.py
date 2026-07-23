from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse
from typing import Annotated, List
from uuid import UUID

from app.auth.jwt_handler import get_current_user
from app.services.post_service import *
from app.exceptions.post_exception import BlogException
from app.schemas.post_schemas import *
from app.repositories.post_repos import base_query


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
# user_id='86c7b890-4811-4786-82e8-49be78f8752e'
# content_id = "64077f70-be09-429c-8eb7-b703f504f366"
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
    class PostRepository:
        def search(self, search):
            params = []
            conditions = []
            limit_offset = []
            order_by = []
            direction = []

            for k, v in search.filters.model_dump(exclude_none=True).items():
                params.append(v)
                conditions.append(f"{k} = %s")

            for k, v in search.sort.model_dump(exclude_none=True).items():
                if k == "by":
                    order_by.append(f"ORDER BY {v}")
                if k == "direction":
                    direction.append(v)

            for k, v in search.pagination.model_dump(exclude_none=True).items():
                if k == "limit":
                    limit_offset.append(f"LIMIT {v}")
                if k == "offset":
                    limit_offset.append(f"OFFSET {v}")
            query = str(base_query) + " AND ".join(conditions) + " " + " ".join(order_by) + " " + " ".join(direction) + " " + " ".join(limit_offset)
            print(query)
        
    post = PostRepository()
    post.search(search)
        

  
