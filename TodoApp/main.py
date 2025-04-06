from fastapi import FastAPI
from TodoApp import models
from TodoApp.database import engine
from TodoApp.routers import auth, todos, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router) #include all routes from auth 
app.include_router(todos.router) #include all routes from todos 
app.include_router(admin.router) #include all routes from admin 
app.include_router(users.router) #include all routes from admin 

