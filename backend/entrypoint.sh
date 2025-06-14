#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h db -p 5432 -U $POSTGRES_USER; do
    echo "PostgreSQL not ready yet, retrying in 2 seconds..."
    sleep 2
done
echo "PostgreSQL is ready!"

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload