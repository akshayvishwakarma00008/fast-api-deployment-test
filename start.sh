
# Make sure Python can find your app
export PYTHONPATH=/opt/render/project/src

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI app..."
uvicorn TodoApp.main:app --host=0.0.0.0 --port=10000 --reload
