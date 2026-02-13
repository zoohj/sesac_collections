# services/tag_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from mysite4.models.tag import Tag
from mysite4.schemas.tag import TagCreate
from mysite4.repositories.tag_repository import tag_repository


class TagService:
    def create_tag(self, db: Session, data: TagCreate):
        with db.begin():
            # 1. 이미 존재하는 태그인지 확인
            existing_tag = tag_repository.find_by_name(db, data.name)
            if existing_tag:
                raise HTTPException(
                    status_code=400, detail="이미 존재하는 태그 이름입니다."
                )

            # 2. 태그 생성 및 저장
            new_tag = Tag(name=data.name)

            tag_repository.save(db, new_tag)

        db.refresh(new_tag)
        return new_tag

    def read_tags(self, db: Session):
        return tag_repository.find_all(db)


tag_service = TagService()
