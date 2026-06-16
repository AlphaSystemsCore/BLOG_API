blog_api_table_preliminary = (
    """
    CREATE TABLE IF NOT EXISTS profile(
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    avatar_link TEXT, 
    social_link TEXT, 
    user_id UUID
    FOREIGN KEY user_id REFERENCES users(user_id)
    )
    """,

    """
    --credentials
    CREATE TABLE IF NOT EXISTS oauth2_credential(
    credential_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL UNIQUE,
    is_verified BOOLEAN DEFAULT 'false',
    created_at TIMESTAMPTZ
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS roles(
    role_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role_name VARCHAR(30)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS preferences(
    preference_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50),
    category VARCHAR(50)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS users_preferences(
    user_id UUID NOT NULL,
    preference_id NOT NULL,
    FOREING KEY user_id REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY preference_id REFERENCES preferences(preference_id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS users(
    user_id UUID PRIMARY KEY gen_random uuid(),
    username VARCHAR(80),
    role_id INTEGER NOT NULL,
    credential_id UUID NOT NULL UNIQUE,
    created_at TIMSTAMPTZ DEFAULT NOW())

    """
)