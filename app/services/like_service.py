from app.repositories.like_repos import create_like_repo
def create_like_service(user_id:str, post_id:str):
    """creates like to a post"""
    updated_row = create_like_repo(user_id, post_id)
    if updated_row:
        return {"msg":"successfully"}
    else:
        raise ValueError("Like not created")

    