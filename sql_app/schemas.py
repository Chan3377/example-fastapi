from datetime import datetime
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Optional
from pydantic.types import conint

# from typing_extensions import Annotated

# create different models for different requests


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    PostBase()
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


# create post Type
class PostCreate(PostBase):
    pass


try:
    PostCreate()
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


# response model by sending back user's email registration
# Define user - not send back data when register user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_model = True


try:
    UserOut()
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


# create response model back for "get post"
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # orm_mode allow pydantic to read any type of data - from FastAPI documentations
    class Config:
        orm_mode = True


try:
    Post()
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


class PostOut(BaseModel):
    Post: Post
    votes: int

    # orm_mode allow pydantic to read any type of data - from FastAPI documentations
    class Config:
        orm_mode = True


try:
    PostOut()
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


# create user
class UserCreate(BaseModel):
    email: EmailStr
    password: str


try:
    UserCreate()
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


class UserLogin(BaseModel):
    email: EmailStr
    password: str


try:
    UserLogin()
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


class Token(BaseModel):
    access_token: str
    token_type: str


try:
    Token()
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


class TokenData(BaseModel):
    id: Optional[int] = None


try:
    TokenData()
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


# le: less than or equal to
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


try:
    Vote()
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))
