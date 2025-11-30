-- Initialize the database schema
CREATE SCHEMA IF NOT EXISTS "secret-santa";

-- Create the secret_friends table
CREATE TABLE IF NOT EXISTS "secret-santa".secret_friends (
    user_id int not null,
    id_secret_friend int not null
);

-- Create the admin table
CREATE TABLE IF NOT EXISTS "secret-santa".admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Note: Admin password is set from ADMIN_PWD environment variable
-- Default username: gota
-- To set password, add ADMIN_PWD to your .env file

