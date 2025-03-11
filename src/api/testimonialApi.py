from typing import List
from fastapi import APIRouter, status, Depends, HTTPException

from src.database.postgres import get_db
from src.model.testimonialModel import TestimonialModel
from src.schema.testimonialSchema import TestimonialCreate, TestimonialResponse
from src.utils.logUtil import log
from sqlalchemy.orm import Session

router = APIRouter()

mock_testimonials = [
    {
        "id": 1,
        "firstName": 'Elena',
        "lastName": 'Ramirez',
        "rating": 4,
        "comment": 'El personal fue muy atento y la clínica es excelente. Mi rodilla se siente mucho mejor.',
    },
    {
        "id": 2,
        "firstName": 'Carlos',
        "lastName": 'Gomez',
        "rating": 5,
        "comment": 'El servicio superó mis expectativas. El Dr. [Apellido del Doctor] es muy conocedor y atento. ¡Muy recomendado!',
    },
    {
        "id": 3,
        "firstName": 'Sofia',
        "lastName": 'Lopez',
        "rating": 3,
        "comment": 'Aceptable, buen servicio en general. Mis sesiones de fisioterapia han sido útiles.',
    },
    {
        "id": 4,
        "firstName": 'Javier',
        "lastName": 'Hernandez',
        "rating": 5,
        "comment": 'Excelente calidad de atención y dedicación. Estoy muy satisfecho con mi recuperación.',
    },
    {
        "id": 5,
        "firstName": 'Isabela',
        "lastName": 'Martinez',
        "rating": 4,
        "comment": 'La clínica es muy limpia y los doctores son muy profesionales. Mi dolor de hombro ha disminuido significativamente.',
    },
    {
        "id": 6,
        "firstName": 'Valentina',
        "lastName": 'Sanchez',
        "rating": 5,
        "comment": 'Todo fue perfecto, desde la recepción hasta el tratamiento. Me sentí muy cómoda.',
    },
    {
        "id": 7,
        "firstName": 'Mateo',
        "lastName": 'Diaz',
        "rating": 4,
        "comment": 'Buen lugar para atención ortopédica. Las instalaciones son modernas y el equipo es amigable.',
    },
    {
        "id": 8,
        "firstName": 'Camila',
        "lastName": 'Ruiz',
        "rating": 3,
        "comment": 'Buen servicio y opciones de tratamiento variadas. Mi espalda se siente mucho mejor.',
    },
    {
        "id": 9,
        "firstName": 'Sebastian',
        "lastName": 'Torres',
        "rating": 5,
        "comment": 'El mejor servicio ortopédico que he recibido. ¡Gracias!',
    },
    {
        "id": 10,
        "firstName": 'Lucia',
        "lastName": 'Vargas',
        "rating": 4,
        "comment": "Muy contenta con el servicio y la calidad de la atención. Mi tobillo está sanando bien."
    }
]


@router.get("/all", response_model=List[TestimonialResponse])
async def get_all_testimonials(db: Session = Depends(get_db)):
    try:
        testimonials = db.query(TestimonialModel).order_by(TestimonialModel.rating.desc()).all()

        if not testimonials:
            log.info("No testimonials found.")
            return []

        # Convert SQLAlchemy objects to Pydantic models
        return [TestimonialResponse.model_validate(testimonial) for testimonial in testimonials]

    except Exception as e:
        log.error(f"Error getting testimonials. Exception: {e}", exc_info=True)
        return []


@router.post("/", response_model=TestimonialResponse, status_code=status.HTTP_201_CREATED)
async def create_testimonial(testimonial: TestimonialCreate, db: Session = Depends(get_db)):
    try:
        new_testimonial = TestimonialModel(
            first_name=testimonial.firstName,
            last_name=testimonial.lastName,
            rating=testimonial.rating,
            comment=testimonial.comment
        )
        db.add(new_testimonial)
        db.commit()
        db.refresh(new_testimonial)

        return new_testimonial

    except Exception as e:
        db.rollback()
        log.error(f"Error creating testimonial. Exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()
