from fastapi import APIRouter

from .email_routes import router as email_router
from .testimonial_routes import router as testimonial_router


# Create a main router to include all route modules
router = APIRouter()

# Include individual routers
router.include_router(email_router, prefix="/email", tags=["email"])
router.include_router(testimonial_router, prefix="/testimonial", tags=["testimonial"])

