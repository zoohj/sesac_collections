# repositories/tag_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from mysite4.models.tag import Tag


class TagRepository:
    def save(self, db: Session, tag: Tag):
        db.add(tag)
        return tag

    def find_all(self, db: Session):
        # scalars().all()을 사용하여 Tag 객체 리스트를 가져온다.
        return db.scalars(select(Tag)).all()

    def find_by_name(self, db: Session, name: str):
        return db.scalar(select(Tag).where(Tag.name == name))


tag_repository = TagRepository()
