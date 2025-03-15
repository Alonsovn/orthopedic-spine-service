from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.postgres import get_db
from src.schemas.user import UserToken, UserCreate, UserLogin
from src.services.user_service import register_user, login_user

router = APIRouter()


@router.post("/register", response_model=UserToken)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)


@router.post("/login", response_model=UserToken)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)
