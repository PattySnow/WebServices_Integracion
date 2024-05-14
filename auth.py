from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from config.db import SessionLocal
from models.model import User as ModelUser
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "c2c9435a9edb9efb2dc1d153fc1755b26cf5f58bb18e48d3ff2d7e53e45d9d06"
ALGORITHM = "HS256"

class User(BaseModel):
    username: str
    fullname: Union[str, None] = None
    email: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(minutes=15)
    else:
        expires = datetime.utcnow() + time_expire
    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(data_copy, key = SECRET_KEY, algorithm = ALGORITHM)
    print(token_jwt)
    return token_jwt

def get_user(db: Session, username: str):
    return db.query(ModelUser).filter(ModelUser.username == username).first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password", headers = {"WWW-Authenticate": "Bearer"})
    return user

def get_user_current(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        token_decode = jwt.decode(token, key = SECRET_KEY, algorithms = [ALGORITHM])
        username = token_decode.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid username or password", headers = {"WWW-Authenticate": "Bearer"})
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired", headers = {"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid username or password", headers = {"WWW-Authenticate": "Bearer"})
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password", headers = {"WWW-Authenticate": "Bearer"})
    return user


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_token({"sub": user.username}, access_token_expires)
    if user:
        print("User authenticated:")
        print("Username:", user.username)
        print("Email:", user.email)
    else:
        print("Authentication failed")
        raise HTTPException(status_code=401, detail="Authentication failed")
        
    return {"access_token": access_token_jwt, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(
    user: User = Depends(get_user_current),
):
    return {"user": user}
