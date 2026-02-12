from sqlalchemy import select
from sqlalchemy.orm import Session

from product_db.models import Product


class ProductRepository:
    def save(self, db: Session, product: Product):
        db.add(product)
        return product

    def find_all(self, db: Session):
        return db.scalars(select(Product)).all()

    def find_by_id(self, db: Session, product_id):
        return db.scalar(select(Product).where(Product.id == product_id))


product_repository = ProductRepository()
