from psycopg2 import errors
from app.repositories.tag_repos import save_tag_repo, get_tags_repo, delete_tag_repo

def create_tag_service(user_id, tag_name, tag_category):
    try:
        save_tag_repo(user_id, tag_name, tag_category)
    except errors.UniqueViolation:
        raise

def delete_tag_service(tag_id):
    delete_tag_repo(tag_id)

def get_tags_service():
    tags = get_tags_repo()
    if not tags:
        return []
    else:
        return tags
    