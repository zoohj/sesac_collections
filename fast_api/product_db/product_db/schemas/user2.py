from pydantic import BaseModel, ConfigDict, Field


class User2CreateRequest(BaseModel):
    nickname: str = Field(..., min_length=2, max_length=50)


class User2Response(BaseModel):
    id: int
    nickname: str

    model_config = ConfigDict(from_attributes=True)
