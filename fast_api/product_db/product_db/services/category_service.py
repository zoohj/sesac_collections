from product_db.models import Category
from product_db.schemas.category import CategoryCreateRequest
from product_db.repositories.category_repository import category_repository
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class CategoryService:
    def create_category(self, db: Session, data: CategoryCreateRequest):
        with db.begin():
            category = category_repository.find_by_name(db, data.name)
            if category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="이미 있는 카테고리",
                )
            new_category = Category(name=data.name)
            category_repository.save(db, new_category)

        # commit 전까지는 new_category는 Name만 가지고잇음, id는 db에서 만들어줌
        db.refresh(new_category)

        return new_category

    def get_categories(self, db: Session):
        return category_repository.find_all(db)


category_service = CategoryService()
