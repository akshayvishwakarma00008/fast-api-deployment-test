#!/bin/bash

# Set path so Python knows how to import your app
export PYTHONPATH=/opt/render/project/src

echo "Running database migrations..."
cd TodoApp
alembic upgrade head
cd ..

echo "Starting FastAPI app..."
uvicorn TodoApp.main:app --host=0.0.0.0 --port=10000 --reload
