from TodoApp.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String(20), nullable=True)


class Todos(Base):
    __tablename__ = 'todos'
    
    id =  Column(Integer, primary_key=True, index=True)
    title  = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
class Test(Base):
    __tablename__ = 'test'
    
    id =  Column(Integer, primary_key=True, index=True)
    name  = Column(String)
    description = Column(String)
    