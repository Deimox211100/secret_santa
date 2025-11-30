#!/bin/bash
# Script to initialize admin user with password from environment variable

set -e

# Wait for postgres to be ready
until pg_isready -h localhost -U ${DB_USER:-postgres}; do
  echo "Waiting for postgres..."
  sleep 2
done

# Set default admin password if not provided
ADMIN_PWD=${ADMIN_PWD:-admin123}

# Replace placeholder in SQL file and execute
envsubst < /docker-entrypoint-initdb.d/admin_setup.sql | psql -U ${DB_USER:-postgres} -d ${DB_NAME:-secret_santa}

echo "Admin user initialized successfully"
