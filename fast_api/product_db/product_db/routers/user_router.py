from fastapi import APIRouter, Depends, status

from database import get_db
from sqlalchemy.orm import Session

# 파일 안에서 만든 '객체' 가져옴
from product_db.schemas.user import UserCreateRequest, UserResponse
from product_db.services.user_service import user_service

router = APIRouter(prefix="/user-db", tags=["user-db"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreateRequest, db: Session = Depends(get_db)):
    return user_service.create_user(db, data)


@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)
