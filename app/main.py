
from fastapi import FastAPI
from app.routes import home

app = FastAPI()
app.include_router(home.router)