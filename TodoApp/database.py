from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# SQLAlCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# SQLAlCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/todo-app-db' # connetion string for postgresql
SQLAlCHEMY_DATABASE_URL = os.getenv('DATABASE_URL') # connetion string for postgresql remote - on railway server

# engine = create_engine(SQLAlCHEMY_DATABASE_URL, connect_args={'check_same_thread':False}) # this is how we connect to sqlite
engine = create_engine(SQLAlCHEMY_DATABASE_URL) # this is how we connect to postgresql
SessionLocal =sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


