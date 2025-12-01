-- ============================================
-- Secret Santa - Supabase Database Setup
-- ============================================
-- Run this in your Supabase SQL Editor
-- Project Settings > Database > SQL Editor

-- 1. Create schema
CREATE SCHEMA IF NOT EXISTS "secret-santa";

-- 2. Create users table
CREATE TABLE IF NOT EXISTS "secret-santa".users (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    deseo1 TEXT NOT NULL,
    link_deseo1 TEXT,
    imagen_deseo1 TEXT,
    deseo2 TEXT NOT NULL,
    link_deseo2 TEXT,
    imagen_deseo2 TEXT,
    deseo3 TEXT,
    link_deseo3 TEXT,
    imagen_deseo3 TEXT,
    character_name VARCHAR(100) NOT NULL UNIQUE,
    character_photo_url TEXT,
    password VARCHAR(255) NOT NULL,
    wishes_locked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. Create secret_friends table
CREATE TABLE IF NOT EXISTS "secret-santa".secret_friends (
    user_id INT NOT NULL,
    id_secret_friend INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES "secret-santa".users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_secret_friend) REFERENCES "secret-santa".users(id) ON DELETE CASCADE
);

-- 4. Create admin table
CREATE TABLE IF NOT EXISTS "secret-santa".admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 5. Insert default admin user
-- IMPORTANT: Change the password after first login!
INSERT INTO "secret-santa".admin (username, password) 
VALUES ('gota', 'change_this_password')
ON CONFLICT (username) DO NOTHING;

-- 6. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_character_name ON "secret-santa".users(character_name);
CREATE INDEX IF NOT EXISTS idx_users_email ON "secret-santa".users(email);
CREATE INDEX IF NOT EXISTS idx_secret_friends_user_id ON "secret-santa".secret_friends(user_id);
CREATE INDEX IF NOT EXISTS idx_secret_friends_friend_id ON "secret-santa".secret_friends(id_secret_friend);

-- 7. Enable Row Level Security (RLS) - Optional but recommended
ALTER TABLE "secret-santa".users ENABLE ROW LEVEL SECURITY;
ALTER TABLE "secret-santa".secret_friends ENABLE ROW LEVEL SECURITY;
ALTER TABLE "secret-santa".admin ENABLE ROW LEVEL SECURITY;

-- 8. Create policies for service role access (allows your app to access data)
-- These policies allow full access when using the service role key
CREATE POLICY "Enable all access for service role" ON "secret-santa".users
    FOR ALL USING (true);

CREATE POLICY "Enable all access for service role" ON "secret-santa".secret_friends
    FOR ALL USING (true);

CREATE POLICY "Enable all access for service role" ON "secret-santa".admin
    FOR ALL USING (true);

-- ============================================
-- Setup Complete!
-- ============================================
-- Next steps:
-- 1. Update your .env file with Supabase credentials
-- 2. Test the connection from your app
-- 3. Change the admin password!
