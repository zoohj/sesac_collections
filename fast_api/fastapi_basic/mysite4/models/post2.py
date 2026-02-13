# mysite4/models/post2.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Post2(Base):
    __tablename__ = "posts2"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # User 외래키: 작성자 정보
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # User와의 관계 설정 (N:1)
    user: Mapped["User"] = relationship(back_populates="posts2")
