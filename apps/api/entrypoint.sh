#!/bin/bash
set -e

echo "Running Database Migrations..."
# In a real environment, wait-for-it or a loop checking postgres connectivity goes here
alembic upgrade head

echo "Starting Application..."
exec "$@"
