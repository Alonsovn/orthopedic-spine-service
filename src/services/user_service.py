from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.user import UserModel
from src.schemas.user import UserCreate, UserLogin
from src.services.auth_service import hash_password, verify_password
from src.utils.logUtil import log


def register_user(user: UserCreate, db: Session):
    log.info(f"Registering user with email: {user.email}")

    existing_user = get_user_by_email(user.email, db)
    if existing_user:
        log.warning(f"Registration failed. User with email {user.email} already exists.")
        raise HTTPException(status_code=400, detail="User already registered with this email")

    hashed_password = hash_password(user.password)
    new_user = UserModel(
        email=user.email,
        hashed_password=hashed_password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        log.info(f"User {user.email} successfully registered")

        return new_user

    except Exception as e:
        log.error(f"Database error: Could not register the user with email {user.email}. Exception {str(e)}",
                  exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error: Could not register the user")


def login_user(user: UserLogin, db: Session):
    log.info(f"User login attempt: {user.email}")

    db_user = get_user_by_email(user.email, db)

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        log.warning(f"Login failed for {user.email}: Not valid credentials")
        return None

    log.info(f"User {user.email} successfully logged in")

    return db_user


def get_user_by_email(email: str, db: Session):
    log.info(f"Fetching user by email: {email}")

    try:
        existing_user = db.query(UserModel).filter(UserModel.email == email).one_or_none()

        return existing_user

    except Exception as e:
        log.error(f"Database error while fetching user {email}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error: Could not fetch user")


def get_user_by_id(user_id: str, db: Session):
    log.info(f"Fetching user by ID: {user_id}")

    try:
        existing_user = db.query(UserModel).filter(UserModel.id == user_id).one_or_none()

        return existing_user

    except Exception as e:
        log.error(f"Database error while fetching user {user_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error: Could not fetch user")