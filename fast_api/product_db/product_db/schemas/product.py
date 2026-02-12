from pydantic import BaseModel, ConfigDict, Field

from product_db.schemas.category import CategoryResponse


class ProductCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: int
    category: str


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int

    model_config = ConfigDict(from_attributes=True)


class ProductResponseWithCategory(ProductResponse):
    category: CategoryResponse
