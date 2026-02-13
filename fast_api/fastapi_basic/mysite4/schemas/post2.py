# mysite4/schemas/post2.py
from pydantic import BaseModel, ConfigDict
from mysite4.schemas.user import UserResponse


class Post2Create(BaseModel):
    title: str
    content: str


class Post2ListResponse(BaseModel):
    id: int
    title: str
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)


class Post2DetailResponse(BaseModel):
    id: int
    title: str
    content: str
    user: UserResponse

    model_config = ConfigDict(from_attributes=True)
