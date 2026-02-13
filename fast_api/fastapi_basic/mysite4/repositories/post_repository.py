# repositories/post_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from mysite4.models import Post, PostTag
from mysite4.schemas.post import PostCreate
from sqlalchemy.orm import selectinload


class PostRepository:
    def save(self, db: Session, new_post: Post):
        # 세션의 작업 목록에 새로운 객체를 추가한다.
        db.add(new_post)
        return new_post

    def find_all(self, db: Session):
        # select 문을 생성하고 scalars를 통해 결과 객체들을 리스트로 가져온다.
        stmt = select(Post)
        return db.scalars(stmt).all()

    def find_all_with_tags(self, db: Session):
        stmt = select(Post).options(
            selectinload(Post.post_tags).joinedload(PostTag.tag)
        )
        return db.scalars(stmt).all()

    def find_by_id(self, db: Session, id: int):
        # 기본키(Primary Key)를 이용한 조회는 db.get이 가장 빠르고 효율적이다.
        return db.get(Post, id)

    def find_by_id_with_details(self, db: Session, id: int):
        post = db.get(
            Post,
            id,
            options=[
                selectinload(Post.comments),  # 1:N 관계에 최적화
                selectinload(Post.post_tags).joinedload(PostTag.tag),
            ],
        )
        return post

    def update(self, db: Session, post: Post, data: PostCreate):
        # 이미 조회된 객체의 속성을 변경하면 세션이 이를 감지한다.
        post.title = data.title
        post.content = data.content
        return post

    def delete(self, db: Session, post: Post):
        # 세션에서 해당 객체를 삭제 대상으로 표시한다.
        db.delete(post)


post_repository = PostRepository()
