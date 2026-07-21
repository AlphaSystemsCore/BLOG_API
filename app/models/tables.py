blog_api_table_production = (
    # --- 1. GLOBAL ENUMS ---
    "CREATE TYPE account_status_type AS ENUM('active', 'deleted', 'revoked')",
    
    "CREATE TYPE posts_status_type AS ENUM('drafted', 'published', 'deleted')",
    
    "CREATE TYPE email_verification_status AS ENUM ('active', 'used', 'expired', 'revoked')",
    
    """
    CREATE TYPE platform_type AS ENUM 
    ('X (Twitter)', 'Telegram', 'Discord', 'GitHub', 'Nostr', 'Farcaster', 'Steemit', 'YouTube', 'LinkedIn', 'Reddit')
    """,

    # --- 2. BASE CORE TABLES ---
    """
    CREATE TABLE IF NOT EXISTS oauth2_credential(
        credential_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        identifier VARCHAR(20) DEFAULT 'email',
        hashed_password TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        deleted_at TIMESTAMPTZ DEFAULT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS roles(
        role_id SERIAL PRIMARY KEY,
        role_name VARCHAR(30) UNIQUE NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS contents(
        content_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        type VARCHAR(50) NOT NULL, -- Shortened from 80 for optimal indexing
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NULL
    )
    """,

    # --- 3. IDENTITY AND PROFILE TABLES ---
    """
    CREATE TABLE IF NOT EXISTS users(
        user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        username VARCHAR(80) NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        account_status account_status_type DEFAULT 'active',
        is_verified BOOLEAN DEFAULT false,
        credential_id UUID NOT NULL UNIQUE,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NULL,
        deleted_at TIMESTAMPTZ DEFAULT NULL, -- Added for Soft Deletes compliance
        FOREIGN KEY (credential_id) REFERENCES oauth2_credential(credential_id) ON DELETE CASCADE
    )
    """,
    
    # Highly specific partial index: ignores deleted/revoked users during normal profile queries
    "CREATE INDEX idx_users_active_status ON users(account_status) WHERE deleted_at IS NULL",

    """
    CREATE TABLE IF NOT EXISTS users_roles(
        user_id UUID NOT NULL,
        role_id INTEGER NOT NULL DEFAULT 1,
        created_at TIMESTAMPTZ DEFAULT NOW(), -- Added Audit Trail tracking
        PRIMARY KEY (user_id, role_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
    )
    """,
    "CREATE INDEX idx_users_roles_role_id ON users_roles(role_id)",

    """
    CREATE TABLE IF NOT EXISTS profile(
        profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        avatar_link TEXT UNIQUE DEFAULT NULL,
        user_id UUID UNIQUE NOT NULL,
        updated_at TIMESTAMPTZ DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS social_handles(
        social_handle_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID NOT NULL,
        social_handle_link TEXT NOT NULL CHECK (social_handle_link ~* '^https?://[^\s/$.?#].[^\s]*$'),
        platform platform_type NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NULL,
        UNIQUE(user_id, platform), -- Ensures exactly 1 link per platform per user
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """,
    "CREATE INDEX idx_social_handles_user ON social_handles(user_id)",

    """
    CREATE TABLE IF NOT EXISTS email_verification(
        token_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- UPGRADED: Changed from serial int to UUID to prevent enumeration attacks
        hashed_email_verification_token TEXT UNIQUE NOT NULL,
        user_id UUID NOT NULL UNIQUE,
        status email_verification_status DEFAULT 'active',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        expire_at TIMESTAMPTZ NOT NULL,
        updated_at TIMESTAMPTZ DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """,

    # --- 4. SYSTEM TAGS ---
    """
    CREATE TABLE IF NOT EXISTS tags(
        tag_id SERIAL PRIMARY KEY,
        user_id UUID NOT NULL, -- Tracks who generated the custom tag
        tag_name VARCHAR(50) NOT NULL UNIQUE,
        tag_category VARCHAR(50) DEFAULT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """,
    "CREATE INDEX idx_tags_user_id ON tags(user_id)",
    "CREATE INDEX idx_tag_category ON tags(tag_category)",

    """
    CREATE TABLE IF NOT EXISTS users_tags(
        user_id UUID NOT NULL,
        tag_id INT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(), -- Added Audit Trail tracking
        PRIMARY KEY (user_id, tag_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
    )
    """,
    "CREATE INDEX idx_users_tags_tag_id ON users_tags(tag_id)",

    # --- 5. APPLICATION DATA (POSTS, LOGISTICS, MEDIA) ---
    """
    CREATE TABLE IF NOT EXISTS posts(
        post_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID NOT NULL,
        content_id UUID NOT NULL UNIQUE,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        is_allowed BOOLEAN DEFAULT true,
        status posts_status_type DEFAULT 'drafted',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NULL,
        deleted_at TIMESTAMPTZ DEFAULT NULL, -- Soft deletion for production safety
        FOREIGN KEY (content_id) REFERENCES contents(content_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """,
    "CREATE INDEX idx_posts_user_id ON posts(user_id)",
    # Partial index: queries your live feed lightning fast by completely skipping soft-deleted posts
    "CREATE INDEX idx_posts_active_feed ON posts(status, created_at DESC) WHERE deleted_at IS NULL",

    """
    CREATE TABLE IF NOT EXISTS media(
        media_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID NOT NULL,
        content_id UUID NOT NULL,
        path TEXT NOT NULL,
        original_filename VARCHAR(255) NOT NULL, -- Increased sizing boundary safely
        file_type VARCHAR(50) NOT NULL, -- Optimized boundary limits
        mime_type VARCHAR(50) NOT NULL, -- Optimized boundary limits
        size BIGINT NOT NULL, -- Changed from INTEGER to BIGINT to cleanly handle files larger than 2GB
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NULL,
        FOREIGN KEY (content_id) REFERENCES contents(content_id) ON DELETE CASCADE, 
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """,
    "CREATE INDEX idx_media_content_id ON media(content_id)",
    "CREATE INDEX idx_media_user_id ON media(user_id)",

    """
    CREATE TABLE IF NOT EXISTS posts_tags(
        post_id UUID NOT NULL,
        tag_id INTEGER NOT NULL,
        PRIMARY KEY (post_id, tag_id),
        FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
    )
    """,
    "CREATE INDEX idx_posts_tags_tag_id ON posts_tags(tag_id)",

    """
    CREATE TABLE IF NOT EXISTS comments (
        comment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        content TEXT NOT NULL,
        content_id UUID NOT NULL, 
        user_id UUID NOT NULL,
        parent_comment_id UUID DEFAULT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NULL,
        deleted_at TIMESTAMPTZ DEFAULT NULL, -- Soft Delete (displays "Comment deleted by user" but preserves structure)
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (content_id) REFERENCES contents(content_id) ON DELETE CASCADE,
        FOREIGN KEY (parent_comment_id) REFERENCES comments(comment_id) ON DELETE CASCADE
    )
    """,
    "CREATE INDEX idx_comments_user_id ON comments(user_id)",
    "CREATE INDEX idx_comments_content_id ON comments(content_id)",
    "CREATE INDEX idx_comments_tree ON comments(parent_comment_id) WHERE deleted_at IS NULL",

    # --- 6. USER INTERACTIONS & AUTH ENTITIES ---
    """
    CREATE TABLE IF NOT EXISTS likes(
        like_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        content_id UUID NOT NULL,
        user_id UUID NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        CONSTRAINT unique_like UNIQUE(content_id, user_id),
        FOREIGN KEY (content_id) REFERENCES contents(content_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """,
    "CREATE INDEX idx_likes_user_id ON likes(user_id)",

    """
    CREATE TABLE IF NOT EXISTS refresh_token(
        refresh_token_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
        hashed_refresh_token TEXT NOT NULL,
        user_id UUID NOT NULL,
        client TEXT NOT NULL,
        is_revoked BOOLEAN DEFAULT false,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        expire_at TIMESTAMPTZ NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """,
    # Highly specialized index: ignores billions of old, expired, or revoked tokens to keep RAM footprint low
    "CREATE INDEX idx_refresh_token_active_lookup ON refresh_token(user_id) WHERE is_revoked = false AND expire_at > NOW()"
)
