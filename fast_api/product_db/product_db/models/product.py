from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .category import Category
    from .wishlist import Wishlist


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    # category클래스 안의 products 변수

    wishlists: Mapped[list["Wishlist"]] = relationship(
        "WishList", back_populates="product"
    )
