from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status

from src.core.app_config import AppConfig
from src.models.user import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_config = AppConfig().config.get("authentication", {})
secret_key = auth_config.get("secretKey", "")
algorithm = auth_config.get("algorithm", "HS256")
access_token_expires_in = auth_config.get("access_token_expire_minutes", 15)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_access_token(user: UserModel, expires_delta: Optional[timedelta] = None) -> str:
    expires_delta = expires_delta or timedelta(minutes=access_token_expires_in)
    expiration = datetime.now(timezone.utc) + expires_delta

    payload = {
        "id": str(user.id),
        "userName": user.name,
        "sub": user.email,
        "exp": expiration.timestamp()
    }
    access_token = jwt.encode(payload, secret_key, algorithm=algorithm)

    return access_token


def decode_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_access_token(token: str) -> dict:
    return decode_token(token)
