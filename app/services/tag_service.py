from psycopg2 import errors
from app.repositories.tag_repos import save_tag_repo, get_tags_repo, delete_tag_repo
from app.exceptions.tag_exceptions import TagNotFoundError

def create_tag_service(user_id, tag_name, tag_category):
    """creating  tags service"""
    try:
        save_tag_repo(user_id, tag_name, tag_category)
    except errors.UniqueViolation:
        raise



def delete_tag_service(tag_id):
    """deleting tags service"""
    row_updated = delete_tag_repo(tag_id)
    if not row_updated:
        raise TagNotFoundError("Tag not found")

def get_tags_service():
    """get tags"""
    tags = get_tags_repo()
    if tags is None:
        raise TagNotFoundError
    else:
        return tags
    