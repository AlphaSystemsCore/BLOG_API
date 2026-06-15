credentials= """
CREATE TABLE IF NOT EXISTS auth_credentials(
credential_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
email TEXT NOT NULL, 
password TEXT NOT NULL,
is_verified BOOLEAN false,
is_revoked BOOLEAN DEFAULT false
);
"""

role_type = "CREATE TYPE rolesType AS ENUM ('user', 'admin')"

users="""
CREATE TABLE IF NOT EXISTS users(
user_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
user_name VARCHAR(100) UNIQUE NOT NULL,
role_id VARCHAR(20) DEFAULT 'user',
credential_id UUID NOT NULL,
FOREIGN KEY credenatial_id REFERENCES auth_credential(credential_id)
)"""

tokens = """
CREATE TABLE IF NOT EXISTS tokens(
hashed_token TEXT,
is_used BOOLEAN DEFAULT false,
expiry TIMESTAMPTZ,
credential_id UUID
)"""