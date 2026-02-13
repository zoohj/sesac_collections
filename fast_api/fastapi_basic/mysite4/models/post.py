from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from database import Base
from typing import TYPE_CHECKING
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy

if TYPE_CHECKING:
    from .comment import Comment
    from .post_tag import PostTag
    from .tag import Tag


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )

    post_tags: Mapped[list["PostTag"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )
    # post.tags로 바로 접근이 가능해집니다.
    tags: AssociationProxy[list["Tag"]] = association_proxy(
        "post_tags", "tag", creator=lambda _tag: PostTag(tag=_tag)
    )
