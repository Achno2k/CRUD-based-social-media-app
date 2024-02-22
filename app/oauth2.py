from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Annotated
from .schemas import TokenData
from .database import get_db
from sqlalchemy.orm import Session
from . import models
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        # print(user_id)
        # print(type(user_id))

        if user_id is None:
            raise credentials_exception
        token_data: str = TokenData(id=str(user_id))
        
        # print(token_data)
        user = db.query(models.User).filter(models.User.id == token_data.id).first()
        # print(user)
        return user
    except JWTError as error:
        # print(error)
        raise credentials_exception
    
    

