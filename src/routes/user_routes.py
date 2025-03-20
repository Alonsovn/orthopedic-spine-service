from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from src.database.postgres import get_db
from src.schemas.user import UserToken, UserCreate, UserLogin
from src.services.auth_service import verify_access_token, \
    generate_user_access_token
from src.services.user_service import register_user, login_user, get_user_by_email
from src.utils.logUtil import log

router = APIRouter()

# OAuth2PasswordBearer: This is used to get the token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register", response_model=UserToken)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    log.info(f"Attempting to register user with email: {user.email}")

    registered_user = register_user(user, db)
    if not registered_user:
        log.error("User registration failed due to a database issue")
        raise HTTPException(status_code=500, detail="Database error: Could not register the user")

    log.info(f"User {user.email} registered successfully")

    user_access_token = generate_user_access_token(registered_user)

    return user_access_token


@router.post("/login", response_model=UserToken)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    log.info(f"Attempting login for user: {user.email}")

    logged_user = login_user(user, db)
    if not logged_user:
        log.warning(f"Login failed for user {user.email}: Invalid credentials")
        raise HTTPException(status_code=401, detail="invalid credentials")

    log.info(f"User {user.email} logged in successfully")

    user_access_token = generate_user_access_token(logged_user)

    return user_access_token


@router.post("/refresh-token", response_model=UserToken)
async def refresh_token(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    log.info("Attempting to refresh token")

    try:
        # Validate the token and extract user info
        payload = verify_access_token(token)
        user_email = payload.get("sub")

        if not user_email:
            log.warning("Refresh token is missing 'sub' field or is invalid.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user_db = get_user_by_email(user_email, db)
        if not user_db:
            log.warning(f"User with email {user_email} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        log.info(f"Successfully refreshed token for user: {user_email}")
        new_access_token = generate_user_access_token(user_db)

        return new_access_token

    except JWTError as e:
        log.error(f"Error during token refresh: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
