from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str  # TODO validate password


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserToken(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None
