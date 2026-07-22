from app.schemas.post_schemas import PostIn

def create_post_service(user_id, post_in: PostIn):
    create_post_repo(user_id,post_in.title, post_in.content)