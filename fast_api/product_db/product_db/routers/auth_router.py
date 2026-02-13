# routers/auth_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from product_db.services.auth_service import auth_service
from product_db.schemas.user2 import (
    UserCreateRequest2,
    UserResponse2,
    TokenResponse,
    UserLogin,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup", response_model=UserResponse2, status_code=status.HTTP_201_CREATED
)
def signup(data: UserCreateRequest2, db: Session = Depends(get_db)):
    return auth_service.signup(db, data)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    access_token = auth_service.login(db, data)
    return {"access_token": access_token}
