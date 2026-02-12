from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .user2 import User2
    from .product import Product


class Wishlist(Base):
    __tablename__ = "wishlist2"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)

    user: Mapped["User2"] = relationship("User2", back_populates="wishlists2")
    product: Mapped["Product"] = relationship("Product", back_populates="wishlists2")
