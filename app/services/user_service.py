from app.repositories.user_repos import get_user_profile_repo

def get_user_profile_service(user_id):
    profile_data = get_user_profile_repo(user_id)