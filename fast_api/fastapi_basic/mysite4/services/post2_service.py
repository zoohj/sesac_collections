# mysite4/services/post2_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from mysite4.repositories.post2_repository import post2_repository
from mysite4.models.post2 import Post2
from mysite4.schemas.post2 import Post2Create
from mysite4.models.user import User


class Post2Service:
    def create_post(self, db: Session, data: Post2Create, current_user: User):
        # 로그인한 유저의 ID를 자동으로 설정한다.
        new_post = Post2(title=data.title, content=data.content, user=current_user)

        post2_repository.save(db, new_post)
        db.commit()  # get_current_user하면서 이미 트랜잭션 시작 -> 수동커밋해야함
        db.refresh(new_post)
        return new_post


post2_service = Post2Service()
