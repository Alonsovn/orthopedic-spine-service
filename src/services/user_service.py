from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.user import UserModel
from src.schemas.user import UserCreate, UserLogin
from src.services.auth_service import hash_password, create_access_token, verify_password


def register_user(user: UserCreate, db: Session):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="There is a user registered with that email")

    hashed_password = hash_password(user.password)
    new_user = UserModel(
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def login_user(user: UserLogin, db: Session):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}