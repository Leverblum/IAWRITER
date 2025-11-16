# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostCreate(BaseModel):
    prompt: str

class PostResponse(BaseModel):
    id: int
    title: str
    body: str
    seo: Optional[str]
    author_id: int
    created_at: datetime

    class Config:
        # Pydantic v2: usar from_attributes en lugar de orm_mode
        from_attributes = True
