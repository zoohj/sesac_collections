# models/comment.py

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(200), nullable=False)

    # 1. 외래키 설정: posts 테이블의 id를 참조한다.
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)

    # 2. 관계 설정: 댓글 객체에서 소속된 게시글 객체로 바로 접근한다.
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments",
    )
