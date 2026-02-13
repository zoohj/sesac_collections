# models/post_tag.py

from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post
    from .tag import Tag

class PostTag(Base):
    __tablename__ = "post_tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # 각각 Post와 Tag를 참조하는 외래키
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))

    # 확장 데이터: 등록일 추가 가능
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    post: Mapped["Post"] = relationship(back_populates="post_tags")
    tag: Mapped["Tag"] = relationship(back_populates="post_tags")