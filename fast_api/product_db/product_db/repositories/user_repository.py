from sqlalchemy import select
from sqlalchemy.orm import Session

from product_db.models.user import User


class UserRepository:
    def save(self, db: Session, user: User):
        db.add(user)
        return user

    def find_all(self, db: Session):
        return db.scalars(select(User)).all()


user_repository = UserRepository()
