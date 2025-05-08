from fastapi import APIRouter

from src.routes import email_routes, testimonial_routes, user_routes, database_routes

# Create a main router to include all route modules
router = APIRouter()
api_version = "/api/v1"

# Include individual routers
router.include_router(email_routes.router, prefix=f"{api_version}/email", tags=["email"])
router.include_router(testimonial_routes.router, prefix=f"{api_version}/testimonial", tags=["testimonial"])
router.include_router(user_routes.router, prefix=f"{api_version}/user", tags=["user"])
router.include_router(database_routes.router, prefix=f"{api_version}/database", tags=["database"])
