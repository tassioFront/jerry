#!/bin/bash
# Docker entrypoint script for running migrations and starting the app

set -e

echo "Waiting for database to be ready..."

# Fix DATABASE_URL if it uses localhost (replace with db for Docker networking)
export DATABASE_URL=$(echo "$DATABASE_URL" | sed 's/@localhost:/@db:/g' | sed 's/@127.0.0.1:/@db:/g')

# Wait for PostgreSQL to be ready using Python (more reliable in containers)
python3 << EOF
import sys
import time
import psycopg2
import os

max_retries = 30
retry_count = 0
db_url = os.getenv('DATABASE_URL', 'postgresql://auth_user:auth_password@db:5432/auth_db')

while retry_count < max_retries:
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        print("PostgreSQL is up!")
        sys.exit(0)
    except psycopg2.OperationalError:
        retry_count += 1
        if retry_count < max_retries:
            time.sleep(1)
        else:
            print("Failed to connect to PostgreSQL after 30 retries")
            sys.exit(1)
EOF

echo "Executing migrations..."

# Run migrations
alembic upgrade head

echo "Migrations completed. Starting application..."

# Execute the main command
exec "$@"

