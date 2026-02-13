from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from database import get_db, engine
from nplusone.models import DemoUser, DemoPost, DemoComment, Base
from nplusone.schemas import (
    PostWithCommentsResponse,
    PostWithUserResponse,
    PostFullResponse,
)

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter(prefix="/nplusone", tags=["N+1 Demo"])


# ============================================
# 1. Posts + User (N:1, joinedload)
# ============================================


@router.get("/posts/with-user", response_model=list[PostWithUserResponse])
def get_posts_with_user_nplusone(db: Session = Depends(get_db)):
    """
    ⚠️ N+1 문제 발생 (Post -> User)

    Post를 조회한 후, 각 Post의 user에 접근할 때마다
    별도의 SELECT 쿼리가 발생합니다.

    쿼리 수: 1 (Posts) + N (각 Post마다 User) = 1 + 6(3) = 7(4)개
    """
    posts = db.scalars(select(DemoPost)).all()
    # [DemoPost, DemoPost, DemoPost, DemoPost, DemoPost]
    # # -> [PostWithUserResponse, PostWithUserResponse, PostWithUserResponse, PostWithUserResponse]
    # for item in [DemoPost, DemoPost, DemoPost, DemoPost, DemoPost]:
    #     PostWithUserResponse(DemoPost) -> post.user를 가져와줘 라는 로직이 숨어있습니다.
    #                                         UserSimpleResponse를 가져와야 하기 때문에.
    #     그때 마다마다 user에 추가적으로 요청을 하게 됩니다.
    return posts


@router.get("/posts/with-user/optimized", response_model=list[PostWithUserResponse])
def get_posts_with_user_optimized(db: Session = Depends(get_db)):
    """
    ✅ joinedload로 N+1 해결 (Post -> User)

    N:1 관계에서는 joinedload가 자연스럽습니다.
    LEFT OUTER JOIN을 사용하여 단일 쿼리로 가져옵니다.

    쿼리 수: 1개 (JOIN)
    """
    stmt = select(DemoPost).options(joinedload(DemoPost.user))
    posts = db.scalars(stmt).all()

    return posts


# ============================================
# 2. Posts + Comments (1:N, selectinload)
# ============================================


@router.get("/posts/with-comments", response_model=list[PostWithCommentsResponse])
def get_posts_with_comments_nplusone(db: Session = Depends(get_db)):
    """
    ⚠️ N+1 문제 발생 (Post -> Comments)

    Post를 조회한 후, 각 Post의 comments에 접근할 때마다
    별도의 SELECT 쿼리가 발생합니다.

    쿼리 수: 1 (Posts) + N (각 Post마다 Comments) = 1 + 6 = 7개
    """
    posts = db.scalars(select(DemoPost)).all()

    return posts


@router.get(
    "/posts/with-comments/optimized", response_model=list[PostWithCommentsResponse]
)
def get_posts_with_comments_optimized(db: Session = Depends(get_db)):
    """
    ✅ selectinload로 N+1 해결 (Post -> Comments)

    1:N 관계에서는 selectinload가 효율적입니다.
    IN 절을 사용하여 중복 없이 데이터를 가져옵니다.

    쿼리 수: 2개 (Posts 1번 + Comments IN 절 1번)
    """
    stmt = select(DemoPost).options(selectinload(DemoPost.comments))
    posts = db.scalars(stmt).all()

    return posts


# ============================================
# 3. Posts + User + Comments (복합)
# ============================================


@router.get("/posts/full", response_model=list[PostFullResponse])
def get_posts_full_nplusone(db: Session = Depends(get_db)):
    """
    ⚠️ N+1 문제 심각하게 발생 (Post -> User + Comments)

    Post를 조회한 후, user와 comments에 접근할 때마다
    별도의 SELECT 쿼리가 발생합니다.

    쿼리 수: 1 (Posts) + 6 (User) + 6 (Comments) = 13개
    """
    posts = db.scalars(select(DemoPost)).all()

    return posts


@router.get("/posts/full/optimized", response_model=list[PostFullResponse])
def get_posts_full_optimized(db: Session = Depends(get_db)):
    """
    ✅ joinedload + selectinload 조합으로 해결

    Post -> User는 joinedload (N:1, JOIN)
    Post -> Comments는 selectinload (1:N, IN 절)

    쿼리 수: 2개 (Post+User JOIN 1번 + Comments IN 절 1번)
    """
    stmt = select(DemoPost).options(
        joinedload(DemoPost.user), selectinload(DemoPost.comments)
    )
    posts = db.scalars(stmt).all()

    return posts


# # ============================================
# # 4. Pagination (페이지네이션)
# # ============================================


@router.get("/posts/paginated/with-user", response_model=Page[PostWithUserResponse])
def get_posts_paginated_with_user(db: Session = Depends(get_db)):
    """
    페이지네이션 + joinedload로 N+1 해결 (Post -> User)

    페이지네이션과 eager loading을 함께 사용하여
    효율적으로 데이터를 가져옵니다.

    쿼리 수: 1개 (JOIN)
    """
    stmt = select(DemoPost).options(joinedload(DemoPost.user))
    return paginate(db, stmt)


@router.get(
    "/posts/paginated/with-comments",
    response_model=Page[PostWithCommentsResponse],
)
def get_posts_paginated_with_comments(db: Session = Depends(get_db)):
    """
    페이지네이션 + selectinload로 N+1 해결 (Post -> Comments)

    페이지네이션과 eager loading을 함께 사용합니다.

    쿼리 수: 2개 (Posts 1번 + Comments IN 절 1번)
    """
    stmt = select(DemoPost).options(selectinload(DemoPost.comments))
    return paginate(db, stmt)


@router.get("/posts/paginated/full", response_model=Page[PostFullResponse])
def get_posts_paginated_full(db: Session = Depends(get_db)):
    """
    페이지네이션 + joinedload + selectinload 조합 (Post -> User + Comments)

    페이지네이션과 함께 최적화된 eager loading 적용

    쿼리 수: 2개 (Post+User JOIN 1번 + Comments IN 절 1번)
    """
    stmt = select(DemoPost).options(
        joinedload(DemoPost.user), selectinload(DemoPost.comments)
    )
    return paginate(db, stmt)


# ============================================
# 0. 데이터베이스 초기화
# ============================================


@router.post("/setup")
def setup_database(db: Session = Depends(get_db)):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    users = [
        DemoUser(id=1, name="Alice"),
        DemoUser(id=2, name="Bob"),
        DemoUser(id=3, name="Charlie"),
    ]
    db.add_all(users)

    posts = [
        DemoPost(id=1, title="Alice의 첫 번째 글", user_id=1),
        DemoPost(id=2, title="Alice의 두 번째 글", user_id=1),
        DemoPost(id=3, title="Bob의 첫 번째 글", user_id=2),
        DemoPost(id=4, title="Bob의 두 번째 글", user_id=2),
        DemoPost(id=5, title="Charlie의 첫 번째 글", user_id=3),
        DemoPost(id=6, title="Charlie의 두 번째 글", user_id=3),
    ]
    db.add_all(posts)

    comments = []
    for post_id in range(1, 7):
        for i in range(1, 4):
            comments.append(
                DemoComment(content=f"Post {post_id}의 댓글 {i}", post_id=post_id)
            )
    db.add_all(comments)

    db.commit()

    return {
        "message": "N+1 데모 데이터 초기화 완료",
        "users": len(users),
        "posts": len(posts),
        "comments": len(comments),
    }


@router.post("/setup/bulk")
def setup_bulk_data(db: Session = Depends(get_db)):
    """
    페이지네이션 테스트를 위한 대량 데이터 추가

    기존 데이터에 추가로:
    - 사용자 12명 (총 15명)
    - 포스트 94개 (총 100개)
    - 댓글 약 380개 (총 400개)
    """
    # 기존 사용자 수 확인
    existing_user_count = db.scalar(select(DemoUser.id).order_by(DemoUser.id.desc()))
    existing_post_count = db.scalar(select(DemoPost.id).order_by(DemoPost.id.desc()))
    existing_comment_count = db.scalar(
        select(DemoComment.id).order_by(DemoComment.id.desc())
    )

    start_user_id = (existing_user_count or 0) + 1
    start_post_id = (existing_post_count or 0) + 1
    start_comment_id = (existing_comment_count or 0) + 1

    # 추가 사용자 12명
    user_names = [
        "David",
        "Eve",
        "Frank",
        "Grace",
        "Henry",
        "Iris",
        "Jack",
        "Kate",
        "Leo",
        "Mary",
        "Nick",
        "Olivia",
    ]
    users = [
        DemoUser(id=start_user_id + i, name=name) for i, name in enumerate(user_names)
    ]
    db.add_all(users)

    # 추가 포스트 생성 (약 94개)
    posts = []
    post_id = start_post_id
    for i, user_id in enumerate(range(start_user_id, start_user_id + len(user_names))):
        post_count = 7 if i < 10 else 8
        for j in range(post_count):
            posts.append(
                DemoPost(
                    id=post_id,
                    title=f"{user_names[i]}의 {j + 1}번째 글",
                    user_id=user_id,
                )
            )
            post_id += 1
    db.add_all(posts)

    # 추가 댓글 생성
    comments = []
    comment_id = start_comment_id
    for post in posts:
        comment_count = 3 if post.id % 3 == 0 else 5
        for i in range(1, comment_count + 1):
            comments.append(
                DemoComment(
                    id=comment_id, content=f"Post {post.id}의 댓글 {i}", post_id=post.id
                )
            )
            comment_id += 1
    db.add_all(comments)

    db.commit()

    return {
        "message": "페이지네이션 테스트용 대량 데이터 추가 완료",
        "added_users": len(users),
        "added_posts": len(posts),
        "added_comments": len(comments),
        "total_users": db.query(DemoUser).count(),
        "total_posts": db.query(DemoPost).count(),
        "total_comments": db.query(DemoComment).count(),
    }
