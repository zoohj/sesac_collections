# schemas/post.py

from pydantic import BaseModel, ConfigDict
from mysite4.schemas.comment import CommentResponse
from mysite4.schemas.tag import TagResponse


class PostCreate(BaseModel):
    title: str
    content: str


class PostCreateWithTags(PostCreate):
    tags: list[str] = []  # ["Python", "FastAPI"] 형태의 태그 이름 리스트


class PostListResponse(BaseModel):
    id: int
    title: str

    # SQLAlchemy 모델 객체를 Pydantic에서 읽기 위한 설정
    model_config = ConfigDict(from_attributes=True)


class PostListWithTagsResponse(PostListResponse):
    tags: list[TagResponse]


class PostDetailResponse(BaseModel):
    id: int
    title: str
    content: str

    comments: list[CommentResponse] = []

    # Post 모델의 association_proxy인 'tags'를 통해 Tag 객체 리스트를 자동으로 매핑한다.
    tags: list[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)
