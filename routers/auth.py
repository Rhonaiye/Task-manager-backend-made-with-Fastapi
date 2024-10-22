import jwt
from datetime import datetime, timedelta, timezone
from models import Users
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, status, HTTPException, Path
from passlib.context import CryptContext
import secrets
from fastapi.security import OAuth2PasswordBearer




router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]


class Usersreq(BaseModel):
    email: str = Field()
    username: str = Field()
    first_name: str = Field()
    last_name: str = Field()
    password: str = Field()
    

class Loginreq(BaseModel):
    username: str
    password: str
    

class TokenData(BaseModel):
    username: str | None = None


    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password:str):
    return pwd_context.hash(password)
       

def verify_pass(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)       


SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(db:db_dependency, token: str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
     
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        
    except:
        raise credentials_exception
    
    user = db.query(Users).filter(Users.username == token_data.username).first()
    
    if user is None:
        raise credentials_exception
    return user
    
    
    
    
    
    
@router.get('/get-users/')
async def get_all_users(db:db_dependency):
    users = db.query(Users).all()
    
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return users
  
    
    
@router.post('/sign-up', status_code=status.HTTP_201_CREATED)
async def users_signup(db:db_dependency, users: Usersreq):
    
    hashed_password = hash_pass(users.password)
    user_model = Users(
        email = users.email,
        username = users.username,
        first_name = users.first_name,
        last_name = users.last_name,
        password = hashed_password
    )
    
    
    db.add(user_model)
    db.commit()
    
    
@router.post('/login', status_code=status.HTTP_200_OK)
async def user_login(db:db_dependency, user_credentials:Loginreq):
    user = db.query(Users).filter(Users.username == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_pass(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    #generate token
    access_token = create_access_token(data= {"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}
    
    
@router.get("/user/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
