import backoff
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

from src.core.app_config import AppConfig
from src.utils.backoff_helper import backoff_handler
from src.utils.logUtil import log


def get_postgres_database_url():
    try:
        postgres_config: dict = AppConfig().config.get("postgres")

        db_username: str = postgres_config.get("username")
        db_password: str = postgres_config.get("password")
        db_host: str = postgres_config.get("host")
        db_port: int = postgres_config.get("port")
        db_name: str = postgres_config.get("dbname")

        return f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

    except KeyError as e:
        log.error(f"Missing configuration for {str(e)}")
        raise ValueError(f"Configuration for {str(e)} is missing in the postgres config.")


@backoff.on_exception(backoff.expo, OperationalError, max_tries=5, on_backoff=backoff_handler)
def create_db_engine():
    database_url = get_postgres_database_url()
    return create_engine(database_url, pool_pre_ping=True)


def init_db():
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        log.info(f"Error initializing database. Exception: {str(e)}")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
