from app.schemas.post_schemas import PostIn, PostOut, FieldsToUpdate
from app.repositories.post_repos import (
    create_post_repo, 
    get_all_post_repo, 
    get_post_by_id_repo, 
    get_post_by_title_repo, 
    get_posts_by_author,
    delete_post_repo, 
    publish_post_repo, 
    update_post_repo 
    )
from app.exceptions.post_exception import *

def create_post_service(user_id, post_in: PostIn) -> dict:
    """Creates a new post, returns created post"""
    post = create_post_repo(user_id, post_in.title, post_in.content)
    if post is None:
        raise PostCreationFailedError("FAILED TO CREATE POST, PLEASE TRY AGAIN")
    return post

# to add pagination later

def get_all_post_service() -> list:
    """returns all published posts"""
    posts = get_all_post_repo()
    if posts is None:
        raise PostNotFoundError("NOT FOUND")
    return posts


def get_post_by_id_service(post_id: str) -> dict:
    """Gets the post by it's  post_id"""
    post = get_post_by_id_repo(post_id)
    if post is None:
        raise PostNotFoundError("NOT FOUND")
    return post

def get_post_by_title_service(title: str) -> list| dict:
    """Gets the post by it's title """
    post = get_post_by_title_repo(title)
    if post is None:
        raise PostNotFoundError("NOT FOUND")
    return post

def get_post_by_author_service(author:str) -> dict | list:
    post = get_posts_by_author(author)
    if post is None:
        raise PostNotFoundError("NOT FOUND")
    return post


def delete_post_service(user_id, post_id) -> dict:
    """Deletes the post by post_id and user_id who created the post"""
    row_updated = delete_post_repo(user_id, post_id)
    if not row_updated:
        raise DeletionFailedError('FIALED TO  DELETE POST')
    return {
        "post_id": post_id,
        "status": "deleted"
    }

def publish_post_service(user_id:str, post_id:str) -> dict  :
    """Make post available pubicly"""
    row = publish_post_repo(user_id, post_id)
    if status != 'published':
        raise PublishPostFailedError("FAILED TO PUBLISH POST")
    return {
        "post_id":post_id,
        "status": row.get('status')
    } 

def update_post_service(user_id:str, to_update: FieldsToUpdate):
    """
        This is a function to update a post
        likes and comments are reseted to zero
    """
    if to_update.title is None and to_update.content is None:
        return {
            "post_id":to_update.post_id,
            "status":"Already up to date"
        }
    post = update_post_repo(user_id, to_update.post_id, to_update.title, to_update.content)
    if post is None:
        raise UpdateFailedError("FAILED TO UPDATE POST")
    return post 