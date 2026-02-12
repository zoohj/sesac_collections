from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from database import Base
from typing import TYPE_CHECKING

from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy


if TYPE_CHECKING:
    from .wishlist import Wishlist


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(10), nullable=False)

    wishlists: Mapped[list["Wishlist"]] = relationship(back_populates="user")

    wishlist_items: AssociationProxy[list["Wishlist"]] = association_proxy(
        "wishlists", "product"
    )
