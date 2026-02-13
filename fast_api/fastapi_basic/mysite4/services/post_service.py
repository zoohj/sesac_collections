# services/post_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from mysite4.repositories.post_repository import post_repository
from mysite4.models.post import Post
from mysite4.schemas.post import PostCreate, PostCreateWithTags
from mysite4.repositories.post_tag_repository import post_tag_repository
from mysite4.repositories.tag_repository import tag_repository
from mysite4.models.post_tag import PostTag
from mysite4.models.tag import Tag


class PostService:
    def create_post(self, db: Session, data: PostCreate):
        new_post = Post(title=data.title, content=data.content)

        # 레포지토리에 저장을 요청한다. (아직 DB에 확정된 상태는 아님)
        post_repository.save(db, new_post)

        # 서비스 계층에서 트랜잭션을 최종 확정한다.
        db.commit()

        # DB에서 생성된 ID 등을 파이썬 객체에 반영한다.
        db.refresh(new_post)

        return new_post

    def read_posts(self, db: Session):
        # return post_repository.find_all(db)
        return post_repository.find_all_with_tags(db)

    def read_post_by_id(self, db: Session, id: int):
        # post = post_repository.find_by_id(db, id)
        post = post_repository.find_by_id_with_details(db, id)
        if not post:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "존재하지 않는 게시글입니다."
            )
        return post

    def update_post(self, db: Session, id: int, data: PostCreate):
        # 수정할 게시글 존재 여부를 먼저 확인한다.
        post = self.read_post_by_id(db, id)

        # 레포지토리를 통해 객체 정보를 수정(더티 체크 대상)한다.
        updated_post = post_repository.update(db, post, data)

        # 최종 확정 및 갱신
        db.commit()
        db.refresh(updated_post)

        return updated_post

    def delete_post(self, db: Session, id: int):
        post = self.read_post_by_id(db, id)

        post_repository.delete(db, post)

        # 삭제 트랜잭션을 확정한다.
        db.commit()

    def add_tag_to_post(self, db: Session, post_id: int, tag_name: str):
        with db.begin():
            # 1. 대상 게시글 조회
            post = self.read_post_by_id(db, post_id)

            # 2. 태그 조회 (없으면 생성: orElseGet 패턴)
            tag = tag_repository.find_by_name(db, tag_name)
            if not tag:
                tag = tag_repository.save(db, Tag(name=tag_name))
                db.flush()  # 생성된 태그의 ID를 확보하기 위해 flush 사용

            # 3. 중복 연결 확인
            if post_tag_repository.exists(db, post.id, tag.id):
                raise HTTPException(
                    status_code=400, detail="이미 이 게시글에 등록된 태그입니다."
                )

            # 4. 연결 객체 생성 및 저장
            new_link = PostTag(post=post, tag=tag)
            post_tag_repository.save(db, new_link)

        return post

    # services/post_service.py

    def create_post_with_tags(self, db: Session, data: PostCreateWithTags):
        # 1. 게시글 객체 생성 (아직 DB 저장 전)
        new_post = Post(title=data.title, content=data.content)

        with db.begin():
            # 2. 태그 처리 로직
            for name in data.tags:
                # 기존 태그 검색 (findByName)
                tag = tag_repository.find_by_name(db, name)

                # 태그가 없으면 새로 생성
                if not tag:
                    tag = Tag(name=name)
                    tag_repository.save(db, tag)
                    db.flush()  # ID 할당을 위해 flush 호출

                # 3. 연결 모델(PostTag) 생성 및 게시글에 추가
                # cascade 설정 덕분에 post_tags에 추가만 하면 나중에 함께 저장된다.
                post_tag_link = PostTag(post=new_post, tag=tag)
                new_post.post_tags.append(post_tag_link)
                # post_tag_repository.save(post_tag_link)

                # 사용자에게 입력받는 추가 컬럼이 없는 경우 아래의 코드도 가능하다.
                # new_post.tags.append(tag)

            # 4. 게시글 저장 (연결된 PostTag들도 함께 저장됨)
            post_repository.save(db, new_post)

        db.refresh(new_post)
        return new_post

    def remove_tag_from_post(self, db: Session, post_id: int, tag_name: str):
        with db.begin():
            # 1. 게시글 조회
            # 또는 self.read_post_by_id
            post = post_repository.find_by_id(db, post_id)
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            # 2. 태그 조회
            # 또는 tag_service.read_tag_by_name 생성 후 호출
            tag = tag_repository.find_by_name(db, tag_name)
            if not tag:
                raise HTTPException(status_code=404, detail="Tag not found")

            # 3. 관계 존재 확인 및 삭제
            if tag not in post.tags:
                raise HTTPException(
                    status_code=400,
                    detail="이 게시글에 해당 태그가 연결되어 있지 않습니다.",
                )

            # Association Proxy를 통해 리스트에서 제거
            # delete-orphan 설정 덕분에 PostTag 레코드가 DB에서 실제로 삭제됨
            post.tags.remove(tag)

        return {"message": f"Tag '{tag_name}' removed from post {post_id}"}


post_service = PostService()
