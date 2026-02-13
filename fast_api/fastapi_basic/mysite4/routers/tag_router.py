# routers/tag_router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from mysite4.schemas.tag import TagCreate, TagResponse
from mysite4.services.tag_service import tag_service

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(data: TagCreate, db: Session = Depends(get_db)):
    return tag_service.create_tag(db, data)


@router.get("", response_model=list[TagResponse])
def read_tags(db: Session = Depends(get_db)):
    return tag_service.read_tags(db)
