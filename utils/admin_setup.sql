-- Add admin table and wishes lock functionality
CREATE TABLE IF NOT EXISTS "secret-santa".admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Add wishes_locked column to track if editing is allowed
ALTER TABLE "secret-santa".users 
ADD COLUMN IF NOT EXISTS wishes_locked BOOLEAN DEFAULT FALSE;

-- Insert default admin (password will be set from ADMIN_PWD environment variable)
-- This is handled by the init-admin.sh script
INSERT INTO "secret-santa".admin (username, password) 
VALUES ('gota', '${ADMIN_PWD}')
ON CONFLICT (username) DO NOTHING;

COMMIT;

