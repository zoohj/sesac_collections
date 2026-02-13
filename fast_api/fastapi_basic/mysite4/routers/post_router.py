# routers/post_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db

from mysite4.services.post_service import post_service
from mysite4.schemas.post import (
    PostCreate,
    PostDetailResponse,
    PostListResponse,
    PostCreateWithTags,
    PostListWithTagsResponse,
)

from mysite4.services.comment_service import comment_service
from mysite4.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(prefix="/posts-db", tags=["posts"])


@router.post("", response_model=PostDetailResponse, status_code=status.HTTP_201_CREATED)
def create_post(data: PostCreate, db: Session = Depends(get_db)):
    # Depends(get_db)를 통해 요청마다 새로운 세션을 주입받는다.
    return post_service.create_post(db, data)


@router.get("", response_model=list[PostListWithTagsResponse])
def read_posts(db: Session = Depends(get_db)):
    return post_service.read_posts(db)


@router.get("/{id}", response_model=PostDetailResponse)
def read_post(id: int, db: Session = Depends(get_db)):
    return post_service.read_post_by_id(db, id)


@router.put("/{id}", response_model=PostDetailResponse)
def update_post(id: int, data: PostCreate, db: Session = Depends(get_db)):
    return post_service.update_post(db, id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_service.delete_post(db, id)


# routers/post_router.py


@router.post(
    "/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(post_id: int, data: CommentCreate, db: Session = Depends(get_db)):
    # 경로에서 받은 post_id를 서비스로 전달한다.
    return comment_service.create_comment(db, post_id, data)


@router.put("/{post_id}/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    post_id: int, comment_id: int, data: CommentCreate, db: Session = Depends(get_db)
):
    updated_comment = comment_service.update_comment(
        db, post_id, comment_id, data.content
    )
    return updated_comment


@router.delete(
    "/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_comment(post_id: int, comment_id: int, db: Session = Depends(get_db)):
    comment_service.delete_comment(db, post_id, comment_id)
    return None


# routers/post_router.py 내 추가


@router.post("/{post_id}/tags/{tag_name}", status_code=status.HTTP_201_CREATED)
def add_tag_to_post(post_id: int, tag_name: str, db: Session = Depends(get_db)):
    post_service.add_tag_to_post(db, post_id, tag_name)
    return {"message": f"Successfully added tag '{tag_name}' to post {post_id}"}


# routers/post_router.py


@router.post(
    "/with-tags", response_model=PostDetailResponse, status_code=status.HTTP_201_CREATED
)
def create_post_with_tags(data: PostCreateWithTags, db: Session = Depends(get_db)):
    return post_service.create_post_with_tags(db, data)


@router.delete("/{post_id}/tags/{tag_name}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tag_from_post(post_id: int, tag_name: str, db: Session = Depends(get_db)):
    post_service.remove_tag_from_post(db, post_id, tag_name)
    return None  # 204 No Content 응답
