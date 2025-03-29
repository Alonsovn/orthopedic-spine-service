from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.core.app_config import AppConfig

auth_config = AppConfig().config.get("authentication")
secret_key = auth_config.get("secretKey")
algorithm = auth_config.get("algorithm")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])

        return payload.get("sub")  # Return user email

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
