# repositories/user_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from mysite4.models.user import User


class UserRepository:
    def save(self, db: Session, user: User):
        db.add(user)
        return user

    def find_by_email(self, db: Session, email: str):
        stmt = select(User).where(User.email == email)
        return db.scalars(stmt).first()

    def find_by_id(self, db: Session, user_id: int):
        return db.get(User, user_id)


user_repository = UserRepository()
