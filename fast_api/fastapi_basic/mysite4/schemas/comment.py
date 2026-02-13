# schemas/comment.py

from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str

    model_config = ConfigDict(from_attributes=True)
