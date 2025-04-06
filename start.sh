
#!/bin/bash

# Run Alembic migrations
echo "Running database migrations..."
alembic upgrade head

# Start the FastAPI app with Uvicorn
echo "Starting FastAPI app..."
uvicorn TodoApp.main:app --host=0.0.0.0 --port=10000 --reload