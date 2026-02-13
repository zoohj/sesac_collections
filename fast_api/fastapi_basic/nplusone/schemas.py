from pydantic import BaseModel, ConfigDict


class UserSimpleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    post_id: int


class PostWithUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    user_id: int
    user: UserSimpleResponse


class PostWithCommentsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    user_id: int
    comments: list[CommentResponse]


class PostFullResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    user_id: int
    user: UserSimpleResponse
    comments: list[CommentResponse]
