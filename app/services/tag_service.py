from psycopg2 import errors
from uuid import UUID

from app.repositories.tag_repos import save_tag_repo, get_tags_repo, delete_tag_repo
from app.exceptions.tag_exceptions import TagOperationalError
from app.schemas.tag_schemas import TagOut, TagIn

def create_tag_service(user_id:UUID, tag_in:TagIn):
    """creating  new tag"""
    try:
        tag = save_tag_repo(user_id, tag_in.tag_name, tag_in.tag_category)
    except errors.UniqueViolation:
        raise
    if tag is None:
        raise TagOperationalError("Failed to create tag")
    return TagOut(*tag)



def delete_tag_service(tag_id:UUID):
    """deleting tag service, only when user is authorized"""
    row_count = delete_tag_repo(tag_id)
    if row_count == 0:
        raise TagOperationalError("Tag not deleted, please try again")
    

def get_tags_service():
    """get tags"""
    tags = get_tags_repo()
    if tags is None:
        raise TagNotFoundError
    else:
        return tags
    