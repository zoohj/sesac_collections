from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class DemoUser(Base):
    __tablename__ = "users_nplusone"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    posts: Mapped[list["DemoPost"]] = relationship(back_populates="user", lazy="select")


class DemoPost(Base):
    __tablename__ = "posts_nplusone"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(ForeignKey("users_nplusone.id"))

    user: Mapped["DemoUser"] = relationship(back_populates="posts")
    comments: Mapped[list["DemoComment"]] = relationship(back_populates="post", lazy="select")


class DemoComment(Base):
    __tablename__ = "comments_nplusone"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(200))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts_nplusone.id"))

    post: Mapped["DemoPost"] = relationship(back_populates="comments")
