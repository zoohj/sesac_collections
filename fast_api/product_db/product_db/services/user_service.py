from sqlalchemy.orm import Session
from product_db.models.user import User
from product_db.repositories.user_repository import user_repository
from product_db.repositories.category_repository import category_repository
from fastapi import HTTPException, status

from product_db.schemas.user import UserCreateRequest


class UserService:
    def create_user(self, db: Session, data: UserCreateRequest):
        with db.begin():
            new_user = User(nickname=data.nickname)
            user_repository.save(db, new_user)

        db.refresh(new_user)
        return new_user

    def get_users(self, db):
        return user_repository.find_all(db)

    def get_user(self, user_id, db):
        return user_repository.find_by_id(db, user_id)


user_service = UserService()
