# mysite4/routers/user_router2.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from product_db.dependencies import get_current_user
from product_db.models.user2 import User2

router = APIRouter(prefix="/wishlist2", tags=["wishlist2"])


# [POST] /wishlist2/{product_id}: 위시리스트 추가
@router.post("/{product_id}", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db), current_user: User2 = Depends(get_current_user)
):
    return user_service.get_users(db)


# [DELETE] /wishlist2/{product_id}: 위시리스트 삭제
