from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.utils.logUtil import log, console_logging_config
from src.api import userApi, reservationApi, emailApi, testimonialApi

app = FastAPI()

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

    log.info("Starting application!")


@app.on_event("startup")
async def init_app():
    init_application()


@app.get("/health")
def get_health_check():
    return {"OK"}


app.include_router(userApi.router, prefix="/user", tags=["user"])
app.include_router(reservationApi.router, prefix="/reservation", tags=["reservation"])

app.include_router(emailApi.router, prefix="/email", tags=["email"])
app.include_router(testimonialApi.router, prefix="/testimonial", tags=["testimonial"])

