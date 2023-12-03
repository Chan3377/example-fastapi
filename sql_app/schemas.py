from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint

# from typing_extensions import Annotated

# create different models for different requests


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# create post Type
class PostCreate(PostBase):
    pass


# response model by sending back user's email registration
# Define user - not send back data when register user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_model = True


# create response model back for "get post"
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # orm_mode allow pydantic to read any type of data - from FastAPI documentations
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    # orm_mode allow pydantic to read any type of data - from FastAPI documentations
    class Config:
        orm_mode = True


# create user
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
    id: Optional[int] = None


# le: less than or equal to
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
