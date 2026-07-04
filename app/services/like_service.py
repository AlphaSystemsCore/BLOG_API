from app.repositories.like_repos import create_like_repo, delete_like_repo, get_total_like_count_repo

# to add and raise better exceptions later

def create_like_service(user_id:str, post_id:str):
    """creates like to a post"""
    updated_row = create_like_repo(user_id, post_id)
    if updated_row:
        return {"msg":"created successfully"}
    else:
        raise ValueError("Like not created")

    
def delete_like_service(user_id, post_id):
    """deletes like using user_id and post_id for only specific post like by user"""
    updated_row = delete_like_repo(user_id, post_id)
    if updated_row:
        return {"msg":"deleted successfully"}
    raise ValueError("like already deleted")

def count_like_service(post_id):
    """counts likes per post"""
    total_likes = get_total_like_count_repo(post_id)
    return {"total_likes": total_likes[0]}