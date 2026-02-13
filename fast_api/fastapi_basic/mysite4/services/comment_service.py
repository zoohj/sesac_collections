# services/comment_service.py

from sqlalchemy.orm import Session
from mysite4.repositories.comment_repository import comment_repository
from mysite4.services.post_service import post_service
from mysite4.models.comment import Comment
from mysite4.schemas.comment import CommentCreate
from fastapi import HTTPException


class CommentService:
    def create_comment(self, db: Session, post_id: int, data: CommentCreate):
        with db.begin():
            # 1. 경로로 받은 post_id가 실제 존재하는 게시글인지 검증
            post = post_service.read_post_by_id(db, post_id)

            # 2. 모델 인스턴스 생성 시 post를 직접 매핑
            new_comment = Comment(content=data.content, post=post)

            comment_repository.save(db, new_comment)

        db.refresh(new_comment)
        return new_comment

    def update_comment(self, db: Session, post_id: int, comment_id: int, content: str):
        with db.begin():
            # # 1. comment_id에 해당하는 Comment 가져오기.
            # comment = comment_repository.find_by_id(db, comment_id)

            # if not comment:
            #     raise HTTPException(status_code=404, detail="Comment not found")

            # if comment.post_id != post_id:
            #     raise HTTPException(
            #         status_code=400, detail="Comment does not belong to this post"
            #     )
            comment = self._get_verified_comment(db, post_id, comment_id)
            # 더티 체킹을 통한 수정
            comment.content = content

        db.refresh(comment)
        return comment

    def delete_comment(self, db: Session, post_id: int, comment_id: int):
        with db.begin():
            # comment = comment_repository.find_by_id(db, comment_id)

            # if not comment:
            #     raise HTTPException(status_code=404, detail="Comment not found")

            # if comment.post_id != post_id:
            #     raise HTTPException(
            #         status_code=400, detail="Comment does not belong to this post"
            #     )
            comment = self._get_verified_comment(db, post_id, comment_id)

            comment_repository.delete(db, comment)


    def _get_verified_comment(self, db: Session, post_id: int, comment_id: int):
        comment = comment_repository.find_by_id(db, comment_id)
        
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        if comment.post_id != post_id:
            raise HTTPException(
                status_code=400, detail="Comment does not belong to this post"
            )

        return comment


comment_service = CommentService()
