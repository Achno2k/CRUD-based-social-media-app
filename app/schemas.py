from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True 

class PostCreate(PostBase):
    pass 

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config():
        from_attributes = True


class PostResponse(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserResponse

    class Config():
        from_attributes = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
