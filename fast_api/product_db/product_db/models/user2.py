from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from database import Base
from typing import TYPE_CHECKING

from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy


if TYPE_CHECKING:
    from .wishlist2 import Wishlist2
    from .product import Product


class User2(Base):
    __tablename__ = "users2"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    nickname: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    wishlists2: Mapped[list["Wishlist2"]] = relationship(
        "Wishlist2", back_populates="user2"
    )
    wishlist_items2: AssociationProxy[list["Product"]] = association_proxy(
        "wishlists2", "product"
    )
