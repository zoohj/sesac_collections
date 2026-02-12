from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreateRequest2(BaseModel):
    email: EmailStr
    nickname: str
    password: str


class UserResponse2(BaseModel):
    id: int
    email: str
    nickname: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
