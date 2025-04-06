
# Run Alembic migrations
echo "Running database migrations..."
cd TodoApp
alembic revision --autogenerate -m "auto migration $(date +%s)"
alembic upgrade head

# Start the FastAPI app with Uvicorn
echo "Starting FastAPI app..."
cd ..
uvicorn TodoApp.main:app --host=0.0.0.0 --port=10000 --reload