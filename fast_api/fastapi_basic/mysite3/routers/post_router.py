from fastapi import APIRouter, status
from mysite3.services.post_service import post_service
from mysite3.schemas.post import PostCreate, PostDetailResponse, PostListResponse

router = APIRouter(prefix="/posts-mvc")


@router.post("", response_model=PostDetailResponse, status_code=status.HTTP_201_CREATED)
def create_post(data: PostCreate):
    return post_service.create_post(data)


@router.get("", response_model=list[PostListResponse])
def read_posts():
    return post_service.read_posts()


@router.get("/{id}", response_model=PostDetailResponse)
def read_post_by_id(id: int):
    return post_service.read_post_by_id(id)


@router.put("/{id}", response_model=PostDetailResponse)
def update_post(id: int, data: PostCreate):
    return post_service.update_post(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_service.delete_post(id)
