from fastapi import APIRouter

router = APIRouter()


@router.get("/all")
async def get_user_all():
    users = {
        "id": 123,
        "name": "Alonso",
        "LastName": "VN"
    }

    return users
