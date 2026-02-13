# routers/async_post_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from async_database import get_async_db
from mysite4.models.post import Post
from mysite4.models.post_tag import PostTag
from mysite4.schemas.post import PostDetailResponse, PostListResponse

router = APIRouter(prefix="/async/posts", tags=["Async Posts (비동기 체험)"])


@router.get("/", response_model=list[PostListResponse])
async def get_posts(db: AsyncSession = Depends(get_async_db)):
    """
    Async 게시글 목록 조회

    쿼리 작성법은 동일하고, await 유무만 다르다!
    """
    stmt = select(Post)
    result = await db.scalars(stmt)  # 비동기!!
    posts = result.all()
    return posts


@router.get("/{post_id}/lazy", response_model=PostDetailResponse)
async def get_post_lazy(post_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    ❌ lazy loading → async에서는 에러 발생!

    sync에서는 post.comments에 접근하면 자동으로 추가 쿼리가 날아가지만,
    async에서는 이벤트 루프 밖에서 동기 I/O를 할 수 없어서 에러 발생:
    → MissingGreenlet: greenlet_spawn has not been called

    """
    post = await db.get(Post, post_id)

    # 여기서 post.comments에 접근하면 lazy loading 시도 → 에러!
    return post


@router.get("/{post_id}/selectin", response_model=PostDetailResponse)
async def get_post_selectin(post_id: int, db: AsyncSession = Depends(get_async_db)):

    stmt = (
        select(Post)
        .where(Post.id == post_id)
        .options(
            selectinload(Post.comments),
            selectinload(Post.post_tags).selectinload(PostTag.tag),
        )
    )
    result = await db.scalars(stmt)
    post = result.one()
    return post
