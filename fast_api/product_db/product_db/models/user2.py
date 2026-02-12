from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from database import Base
from typing import TYPE_CHECKING

from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy


if TYPE_CHECKING:
    from .wishlist2 import Wishlist2


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(10), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    wishlists2: Mapped[list["Wishlist2"]] = relationship(back_populates="user")

    wishlist_items2: AssociationProxy[list["Wishlist2"]] = association_proxy(
        "wishlists2", "product"
    )
