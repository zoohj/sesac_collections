# mysite4/routers/user_router2.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from product_db.schemas.user2 import UserResponse2
from product_db.models.user import User
from product_db.dependencies import get_current_user

router = APIRouter(tags=["Users"])


@router.get("/me", response_model=UserResponse2)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# [GET] /me/wishlist: 내 위시리스트 목록 조회
