#!/bin/bash
# Script to initialize test database in Docker

set -e

echo "Creating test database if it doesn't exist..."

# Create test database
PGPASSWORD=${POSTGRES_PASSWORD:-auth_password} psql -h db -U ${POSTGRES_USER:-auth_user} -d postgres <<-EOSQL
    SELECT 'CREATE DATABASE auth_test_db'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'auth_test_db')\gexec
EOSQL

echo "Test database ready!"


