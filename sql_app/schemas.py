from datetime import datetime
from pydantic import BaseModel, EmailStr, ValidationError, ConfigDict
from typing import Optional
from pydantic.types import conint

# from typing_extensions import Annotated

# create different models for different requests


class PostBase(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    title: str
    content: str
    published: bool = True


try:
    PostBase(title="Post", content="content", published=True)
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


# create post Type
class PostCreate(PostBase):
    # model_config = ConfigDict(from_attributes=True)
    pass


try:
    PostCreate(PostBase=PostBase(title="Post", content="content", published=True))
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


# response model by sending back user's email registration
# Define user - not send back data when register user
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    created_at: datetime

    # class Config:
    #     orm_model = True


try:
    UserOut(id=1, email="email@gmail.com", created_at="2032-04-23T10:20:30.400+02:30")
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


# create response model back for "get post"
class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # orm_mode allow pydantic to read any type of data - from FastAPI documentations
    # class Config:
    #     orm_mode = True


try:
    Post(
        id=1,
        created_at="2032-04-23T10:20:30.400+02:30",
        owner_id=1,
        owner={
            "id": 1,
            "email": "email@gmail.com",
            "created_at": "2032-04-23T10:20:30.400+02:30",
        },
    )
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    Post: Post
    votes: int

    # orm_mode allow pydantic to read any type of data - from FastAPI documentations
    # class Config:
    #     orm_mode = True


try:
    PostOut(
        Post={
            "id": 1,
            "created_at": "2032-04-23T10:20:30.400+02:30",
            "owner_id": 1,
            "owner": {
                "id": 1,
                "email": "email@gmail.com",
                "created_at": "2032-04-23T10:20:30.400+02:30",
            },
        },
        votes=0,
    )
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


# create user
class UserCreate(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    password: str


try:
    UserCreate(email="email@gmail.com", password="password")
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


class UserLogin(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    password: str


try:
    UserLogin(email="email@gmail.com", password="password")
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


class Token(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str


try:
    Token(access_token="str", token_type="str")
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


class TokenData(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None


try:
    TokenData(id=None)
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))


# le: less than or equal to
class Vote(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    post_id: int
    dir: conint(le=1)


try:
    Vote(post_id=1, dir=1)
except ValidationError as exc:
    print(repr(exc.errors()[0]["type"]))
