from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str  # TODO validate password


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserTokenResponse(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    token_type: str = Field(..., alias="tokenType")
    refresh_token: Optional[str] = Field(..., alias="refreshToken")


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., alias="refreshToken")
