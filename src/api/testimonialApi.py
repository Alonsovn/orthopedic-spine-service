from typing import List

from fastapi import APIRouter, status

from src.schema.testimonialSchema import TestimonialCreate, TestimonialResponse
from src.utils.logUtil import log

router = APIRouter()

mock_testimonies = [
    {
        "id": 1,
        "firstName": 'Elena',
        "lastName": 'Ramirez',
        "rating": 4,
        "testimony": 'El personal fue muy atento y la clínica es excelente. Mi rodilla se siente mucho mejor.',
    },
    {
        "id": 2,
        "firstName": 'Carlos',
        "lastName": 'Gomez',
        "rating": 5,
        "testimony": 'El servicio superó mis expectativas. El Dr. [Apellido del Doctor] es muy conocedor y atento. ¡Muy recomendado!',
    },
    {
        "id": 3,
        "firstName": 'Sofia',
        "lastName": 'Lopez',
        "rating": 3,
        "testimony": 'Aceptable, buen servicio en general. Mis sesiones de fisioterapia han sido útiles.',
    },
    {
        "id": 4,
        "firstName": 'Javier',
        "lastName": 'Hernandez',
        "rating": 5,
        "testimony": 'Excelente calidad de atención y dedicación. Estoy muy satisfecho con mi recuperación.',
    },
    {
        "id": 5,
        "firstName": 'Isabela',
        "lastName": 'Martinez',
        "rating": 4,
        "testimony": 'La clínica es muy limpia y los doctores son muy profesionales. Mi dolor de hombro ha disminuido significativamente.',
    },
    {
        "id": 6,
        "firstName": 'Valentina',
        "lastName": 'Sanchez',
        "rating": 5,
        "testimony": 'Todo fue perfecto, desde la recepción hasta el tratamiento. Me sentí muy cómoda.',
    },
    {
        "id": 7,
        "firstName": 'Mateo',
        "lastName": 'Diaz',
        "rating": 4,
        "testimony": 'Buen lugar para atención ortopédica. Las instalaciones son modernas y el equipo es amigable.',
    },
    {
        "id": 8,
        "firstName": 'Camila',
        "lastName": 'Ruiz',
        "rating": 3,
        "testimony": 'Buen servicio y opciones de tratamiento variadas. Mi espalda se siente mucho mejor.',
    },
    {
        "id": 9,
        "firstName": 'Sebastian',
        "lastName": 'Torres',
        "rating": 5,
        "testimony": 'El mejor servicio ortopédico que he recibido. ¡Gracias!',
    },
    {
        "id": 10,
        "firstName": 'Lucia',
        "lastName": 'Vargas',
        "rating": 4,
        "testimony": "Muy contenta con el servicio y la calidad de la atención. Mi tobillo está sanando bien."
    }
]


@router.get("/", response_model=List[TestimonialResponse])
async def get_all_testimonials():
    try:
        return mock_testimonies

    except Exception as e:
        log.info(f"Error getting opinions. Exception: {e}")


@router.post("/", response_model=TestimonialResponse, status_code=status.HTTP_201_CREATED)
async def create_testimony(testimonial: TestimonialCreate):
    try:
        new_id = len(mock_testimonies) + 1
        new_testimonial = {"id": new_id, **testimonial.model_dump()}
        mock_testimonies.append(new_testimonial)

        return new_testimonial

    except Exception as e:
        log.info(f"Error getting opinions. Exception: {e}")
