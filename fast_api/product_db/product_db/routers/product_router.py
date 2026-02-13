from fastapi import APIRouter, Depends, status

from database import get_db
from sqlalchemy.orm import Session

# 파일 안에서 만든 '객체' 가져옴
from product_db.schemas.product import (
    ProductCreateRequest,
    ProductResponseWithCategory,
)
from product_db.services.product_service import product_service

router = APIRouter(prefix="/product-db", tags=["product-db"])


@router.post(
    "", response_model=ProductResponseWithCategory, status_code=status.HTTP_201_CREATED
)
def create_product(data: ProductCreateRequest, db: Session = Depends(get_db)):
    return product_service.create_product(db, data)


@router.get("", response_model=list[ProductResponseWithCategory])
def get_products(db: Session = Depends(get_db)):
    return product_service.get_products(db)


@router.get("/{product_id}", response_model=ProductResponseWithCategory)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, product_id)
