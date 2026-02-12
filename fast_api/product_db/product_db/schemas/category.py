from pydantic import BaseModel, ConfigDict, Field


class CategoryCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
