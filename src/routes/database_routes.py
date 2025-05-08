from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.postgres import get_db

router = APIRouter()


@router.get("/health/db")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Database connection"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
