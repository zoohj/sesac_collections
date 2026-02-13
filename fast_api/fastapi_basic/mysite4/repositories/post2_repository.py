# mysite4/repositories/post2_repository.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from mysite4.models.post2 import Post2
from mysite4.schemas.post2 import Post2Create


class Post2Repository:
    def save(self, db: Session, new_post: Post2):
        db.add(new_post)
        return new_post


post2_repository = Post2Repository()
