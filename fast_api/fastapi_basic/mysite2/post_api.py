# post_api.py
from fastapi import APIRouter, status, HTTPException
from .post import PostCreate, Post, PostDetailResponse, PostListResponse

# 경로 접두사 설정
router = APIRouter(prefix="/posts-pydantic")

# 게시글 저장소 역할을 수행하는 리스트
posts = []

posts.append(Post(1, "기본 제목", "기본 내용"))
posts.append(Post(2, "기본 제목", "기본 내용"))
posts.append(Post(3, "기본 제목", "기본 내용"))
post_id = 3


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PostDetailResponse)
def create_post(post_data: PostCreate):
    # post_data에는 제목, 내용이라는 필드만 들어가야 합니다.
    # basemodel을 통해 제목, 내용만 들어있도록 강제한다.
    global post_id
    post_id += 1

    if post_data.title == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="title을 입력하세요",
        )

    if post_data.content == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="content을 입력하세요",
        )

    post = Post(post_id, post_data.title, post_data.content)

    posts.append(post)

    return post


@router.get("", response_model=list[PostListResponse])
# @router.get("")
def read_posts():
    # 저장된 모든 게시글 반환
    return posts


# 검색기능을 만들어볼까 합니다.
# 검색어를 입력받아서 그에 해당하는 post를 return하는 api
# /search?keyword=검색어
@router.get("/search")
def search_posts(keyword: str):
    if keyword:
        # 제목에 키워드가 포함된 글만 골라내기
        return [p for p in posts if keyword in p.title]


@router.get("/{id}", response_model=PostDetailResponse)
def read_post(id: int):
    # 식별자가 일치하는 데이터를 리스트에서 탐색
    for post in posts:
        if post.id == id:
            return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다."
    )



# post_api.py 내부에 추가


@router.put("/{id}")
def update_post(id: int, updated_post: PostCreate):
    if updated_post.title == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="title을 입력하세요",
        )

    if updated_post.content == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="content을 입력하세요",
        )

    for post in posts:
        if post.id == id:
            # 전달받은 객체의 필드값으로 기존 데이터 갱신
            post.title = updated_post.title
            post.content = updated_post.content
            return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다."
    )


# post_api.py 내부에 추가


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for index, post in enumerate(posts):
        if post.id == id:
            # 해당 인덱스의 요소를 추출하여 제거
            posts.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다."
    )


# #특정 유저가 작성한 게시글
# @router.get("users/{user_id}/posts", response_model=list[PostListResponse])
# @router.get("posts?user_id=user_id", response_model=list[PostListResponse])
# def func(user_id)
#     return posts
