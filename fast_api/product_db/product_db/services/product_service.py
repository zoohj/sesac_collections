from sqlalchemy.orm import Session
from product_db.models.product import Product
from product_db.repositories.product_repository import product_repository
from product_db.repositories.category_repository import category_repository
from product_db.schemas.product import ProductCreateRequest
from fastapi import HTTPException, status


class ProductService:
    def create_product(self, db: Session, data: ProductCreateRequest):
        with db.begin():
            category = category_repository.find_by_name(db, data.category)
            if category:
                print(f"찾은 카테고리 ID: {category.id}")  # 이게 1이 맞는지 확인
            if not category:
                raise HTTPException(
                    status_code=400,
                    detail=f"'{data.category}' 카테고리를 찾을 수 없습니다. 먼저 카테고리를 생성하세요.",
                )
            new_product = Product(name=data.name, price=data.price, category=category)

            product_repository.save(db, new_product)
            db.flush()
            db.refresh(new_product)
        return new_product

    def get_products(self, db):
        return product_repository.find_all(db)

    def get_product(self, product_id, db):
        return product_repository.find_by_id(product_id, db)


product_service = ProductService()
