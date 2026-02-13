from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class WishlistCreateRequest(BaseModel):
    email: str
    password: str


class WishlistResponse(BaseModel):
    
