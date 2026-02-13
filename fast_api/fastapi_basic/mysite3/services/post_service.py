from mysite3.repositories.post_repository import post_repository
from mysite3.schemas.post import Post, PostCreate
from fastapi import HTTPException, status


class PostService:
    def create_post(self, data: PostCreate):
        # data에 대한 검증 등등을 시행

        if data.title == "":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="title을 입력하세요",
            )

        if data.content == "":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="content을 입력하세요",
            )

        new_post = Post(title=data.title, content=data.content)

        return post_repository.save(new_post)

    def read_posts(self):
        # 나중에 비즈니스 로직이 추가면 여기가 채워질 예정.
        return post_repository.find_all()

    def read_post_by_id(self, id: int):
        # id에 해당하는 데이터가 있다면 데이터 전달할게
        # id에 해당하는 데이터가 없다면 error raise할게.
        post = post_repository.find_by_id(id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return post

    def update_post(self, id: int, data: PostCreate):
        # 서비스의 입장에서는
        # 1. id에 해당하는 post가 있는지 확인한다.
        # 2. 그게 있다면 수정한다.

        # 1. -> 없다면 예외처리가 됩니다.
        # 다른 서비스를 호출 / 여러 개의 repository를 호출
        self.read_post_by_id(id)


        if data.title == "":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="title을 입력하세요",
            )

        if data.content == "":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="content을 입력하세요",
            )

        # 2.
        return post_repository.modify(id, data)


    def delete_post(self, id: int):
        self.read_post_by_id(id)
        post_repository.delete(id)



post_service = PostService()
