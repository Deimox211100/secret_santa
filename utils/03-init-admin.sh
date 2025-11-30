#!/bin/bash
# Script to initialize admin with password from environment variable

set -e

# Wait a moment for postgres to be fully ready
sleep 2

# Get admin password from environment or use default
ADMIN_PWD=${ADMIN_PWD:-admin123}

echo "Initializing admin user..."

# Execute SQL with environment variable substitution
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Add admin table if not exists
    CREATE TABLE IF NOT EXISTS "secret-santa".admin (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    );

    -- Add wishes_locked column to track if editing is allowed
    ALTER TABLE "secret-santa".users 
    ADD COLUMN IF NOT EXISTS wishes_locked BOOLEAN DEFAULT FALSE;

    -- Insert default admin with password from environment
    INSERT INTO "secret-santa".admin (username, password) 
    VALUES ('gota', '$ADMIN_PWD')
    ON CONFLICT (username) DO NOTHING;
EOSQL

echo "Admin user initialized successfully with username: gota"
