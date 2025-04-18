from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from TodoApp.models import Users
from passlib.context import CryptContext # for passsword hashing
from sqlalchemy.orm import Session
from TodoApp.database import SessionLocal
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
SECRET_KEY = '7f1f4d19a6c6e72ecbfe278f64e38ca7ffa9b63110486142f4ac42ae205b5bbc'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto') #setting up bcrypt
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

#generate a access token
def create_access_token(username: str, user_id: int, role:str, expires_delta: timedelta):
    encode = {
        'sub': username,
        'id': user_id,
        'role': role,
    }
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expire})
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if user_id is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
        
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
            
        
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, create_user_request:CreateUserRequest):
    print("Creating user", create_user_request)
    create_user_model = Users(
        email =  create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password), # hashing the passowrd
        is_active = True
    )
    
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    
    return create_user_model

#token generation
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user')
    
    token = create_access_token (user.username, user.id, user.role, timedelta(minutes=20))
    return {
        'access_token': token,
        'token_type': 'bearer',
    }
    
