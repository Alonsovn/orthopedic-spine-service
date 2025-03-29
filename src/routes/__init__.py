from fastapi import APIRouter

from src.routes import email_routes, testimonial_routes, user_routes

# Create a main router to include all route modules
router = APIRouter()

# Include individual routers
router.include_router(email_routes.router, prefix="/email", tags=["email"])
router.include_router(testimonial_routes.router, prefix="/testimonial", tags=["testimonial"])
router.include_router(user_routes.router, prefix="/user", tags=["user"])
