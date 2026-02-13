# routers/user_router.py

from fastapi import APIRouter, Depends, status
from mysite4.dependencies import get_current_user
from mysite4.models import User
from mysite4.schemas.user import UserResponse

router = APIRouter(prefix="")


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
