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
    hashed_password TEXT NOT NULL,
    is_verified BOOLEAN DEFAULT false,
    is_revoked BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS email_verification(
    token_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hashed_token TEXT NOT NULL,
    credential_id UUID NOT NULL,
    is_used BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,

    )
    """
    """
    CREATE TABLE IF NOT EXISTS roles(
    role_id  SERIAL PRIMARY KEY,
    role_name VARCHAR(30) UNIQUE NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS preferences(
    preference_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    category VARCHAR(50)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS users_preferences(
    user_id UUID NOT NULL,
    preference_id INT NOT NULL,
    PRIMARY KEY (user_id, preference_id)
    FOREING KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ,
    FOREIGN KEY (preference_id) REFERENCES preferences(preference_id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS users(
    user_id UUID PRIMARY KEY gen_random_uuid(),
    username VARCHAR(80),
    role_id INTEGER NOT NULL,
    credential_id UUID NOT NULL UNIQUE,
    created_at TIMSTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ ---ILL MAKE AUTOMATIC
    FOREIGN KEY credential_id REFERENCES oauth2_credential(credential_id),
    FOREIGN KEY role_id REFERENCES roles(role_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS email_verification_token(
    token_id UUID PRIMARY KEY gen_random_uuid(),
    hashed_token TEXT NOT NULL,
    credential_id UUID NOT NULL,
    is_used BOOLEAN DEFAULT 'false',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expire_at TIMESTAMPTZ NOT NULL
    )
    """,
    "CREATE TYPE status_types AS ENUM('drafted', 'published', 'deleted')",
    """
    CREATE TABLE IF NOT EXISTS posts(
    post_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title TEXT NOT NULL,
    content NOT NULL,
    image_link TEXT,
    social_link TEXT,
    tag_id INT,
    is_allowed BOOLEAN DEFAULT true,
    status status_type DEFAULT 'drafted',
    created_at TIMESTAMPZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    FOREIGN KEY tag_id REFERENCES tags(tag_id),
    FOREIGN KEY user_id REFERENCES user(user_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS comments(
    comment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    post_id UUID NOT NULL, 
    user_id UUID NOT NULL,
    parent_comment_id UUID FOREIGN KEY REFERENCES comments(comment_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    FOREIGN KEY user_id REFERENCES users(user_id)
    FOREIGN KEY post_id REFERENCED posts(post_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS likes(
    like_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL,
    user_id UUID NOT NULL,
    created_at TIMESTAMPZ DEFAULT NOW(),
    CONSTRAINT UNIQUE(post_id, user_id),
    FOREIGN KEY post_id REFERENCES post,
    FOREIGN KEY users_id REFERENCES users
    )
    """
)