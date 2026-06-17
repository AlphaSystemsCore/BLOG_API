blog_api_table_preliminary = (
     """
    --credentials
    CREATE TABLE IF NOT EXISTS oauth2_credential(
    credential_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS roles(
    role_id  SERIAL PRIMARY KEY,
    role_name VARCHAR(30) UNIQUE NOT NULL
    )
    """,

   

    """
    CREATE TABLE IF NOT EXISTS users(
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(80),
    email TEXT NOT NULL UNIQUE,
    account_status account_status_type DEFAULT 'active',
    role_id INTEGER DEFAULT 1,
    credential_id UUID NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    FOREIGN KEY (credential_id) REFERENCES oauth2_credential(credential_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS profile(
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    avatar_link TEXT, 
    social_link TEXT, 
    user_id UUID UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """,

   
    """
    CREATE TABLE IF NOT EXISTS email_verification(
    token_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hashed_token TEXT NOT NULL,
    user_id UUID NOT NULL,
    is_used BOOLEAN DEFAULT false,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    FOREIGN KEY (user_id)  REFERENCES users(user_id)

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
    PRIMARY KEY (user_id, preference_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ,
    FOREIGN KEY (preference_id) REFERENCES preferences(preference_id) ON DELETE CASCADE
    )
    """,


    """
    CREATE TABLE IF NOT EXISTS posts(
    post_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    image_link TEXT,
    social_link TEXT,
    tag_id INT,
    is_allowed BOOLEAN DEFAULT true,
    status status_type DEFAULT 'drafted',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    FOREIGN KEY (tag_id) REFERENCES preferences(preference_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS comments (
    comment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    post_id UUID NOT NULL, 
    user_id UUID NOT NULL,
    parent_comment_id UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_comment_id) REFERENCES comments(comment_id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS likes(
    like_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL,
    user_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_like UNIQUE(post_id, user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """
)
#  "CREATE TYPE IF NOT EXISTS account_status_type AS ENUM('active', 'deleted', 'revoked')",
    # --"CREATE TYPE IF NOT EXISTS status_type AS ENUM('drafted', 'published', 'deleted')",