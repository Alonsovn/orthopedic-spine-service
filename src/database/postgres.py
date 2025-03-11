import os

import backoff
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.utils.backoff_helper import backoff_handler

db_username = "admin"
db_password = os.getenv("POSTGRES_PASSWORD")
db_port = 5432
db_name = "orthopedic_spine_db"
# db_host = "postgres"
db_host = "localhost"

DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Create tables if they don't exist

def init_db():
    Base.metadata.create_all(bind=engine)


@backoff.on_exception(backoff.expo, OperationalError, max_tries=5, on_backoff=backoff_handler)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
