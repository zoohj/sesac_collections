# repositories/post_tag_repository.py

from sqlalchemy import select
from sqlalchemy.orm import Session
from mysite4.models.post_tag import PostTag

class PostTagRepository:
    def save(self, db: Session, post_tag: PostTag):
        db.add(post_tag)
        return post_tag

    # find_by_id처럼 활용한 후, service에서 처리해도 되긴 합니다.
    def exists(self, db: Session, post_id: int, tag_id: int):
        # 이미 해당 게시글에 해당 태그가 있는지 확인
        stmt = select(PostTag).where(
            PostTag.post_id == post_id, PostTag.tag_id == tag_id
        )
        return db.scalar(stmt) is not None

post_tag_repository = PostTagRepository()