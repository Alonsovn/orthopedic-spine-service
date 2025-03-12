from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.database.postgres import init_db
from src.routes import email_routes, testimonial_routes
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
    init_db()
    log.info("Starting application!")


@app.on_event("startup")
async def init_app():
    init_application()


@app.get("/health")
def get_health_check():
    return {"OK"}


app.include_router(api_router)
