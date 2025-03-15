import subprocess

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.database.postgres import init_db
from src.utils.logUtil import log, console_logging_config

from src.routes import router as api_router

app = FastAPI(title="Orthopedic Spine Service")

origins = [
    "http://localhost:5173",  # Add your React app's URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def init_application():
    console_logging_config()
    run_db_migrations()
    init_db()


@app.on_event("startup")
async def init_app():
    log.info("Starting application!")
    init_application()


def run_db_migrations():
    try:
        log.info("Running alembic migrations..")
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        log.info("Database migrations applied successfully.")
    except subprocess.CalledProcessError as e:
        log.error(f"Error applying migrations. Exception:  {str(e)}")

@app.get("/health")
def get_health_check():
    return {"OK"}


app.include_router(api_router)
