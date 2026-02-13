# repositories/comment_repository.py

from sqlalchemy.orm import Session
from mysite4.models.comment import Comment

class CommentRepository:
    def save(self, db: Session, new_comment: Comment):
        # 세션의 작업 목록에 새로운 댓글 객체를 추가한다.
        db.add(new_comment)
        return new_comment

    def find_by_id(self, db: Session, comment_id: int):
        return db.get(Comment, comment_id)

    def delete(self, db: Session, comment: Comment):
        db.delete(comment)


comment_repository = CommentRepository()