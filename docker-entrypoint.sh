#!/usr/bin/env bash
set -e

echo "Waiting for database to be ready..."

# Require POSTGRES_* or DATABASE_URL to be set
if [ -z "$DATABASE_URL" ]; then
  if [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ] || [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_HOST" ] || [ -z "$POSTGRES_PORT" ]; then
    echo "ERROR: DATABASE_URL is not set and one or more POSTGRES_* env vars are missing."
    echo "Required: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT"
    exit 1
  fi
  export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
fi

export DB_URL="$DATABASE_URL"

python3 << 'EOF'
import sys
import time
import os
import psycopg2

db_url = os.getenv("DB_URL")
max_retries = 30

for attempt in range(1, max_retries + 1):
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        print("PostgreSQL is up!")
        sys.exit(0)
    except psycopg2.OperationalError as e:
        if attempt == max_retries:
            print(f"Failed to connect to PostgreSQL after {max_retries} retries: {e}")
            sys.exit(1)
        time.sleep(1)
EOF

echo "Executing migrations..."
alembic upgrade head

echo "Migrations completed. Starting application..."
exec "$@"
