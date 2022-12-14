
from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic import conint

class ModelPost(BaseModel):
    title: str
    content: str
    published: bool = True



class PostCreate(ModelPost):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class ResponsePost(ModelPost):
    id:int
    owner_id:int
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir :conint(le=1)

class PostOut(BaseModel):
    Post: ResponsePost
    votes: int

    class Config:
        orm_mode = True
