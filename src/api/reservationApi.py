from fastapi import APIRouter, HTTPException
from src.model.reservationModel import ReservationModel
from src.utils.logUtil import log

router = APIRouter()

reservations = [ReservationModel(123, "reservation1", "email1@gmail.com", "message1")]


@router.get("/all")
async def get_reservation_all():
    return reservations


@router.get("/{reservation_id}")
async def get_reservation_by_id(reservation_id: int):
    for reservation in reservations:
        if reservation.reservation_id == reservation_id:
            return reservation

    raise HTTPException(status_code=404, detail="Reservation not found")


@router.post("/post")
async def create_reservation(reservation: ReservationModel):
    reservations.append(reservation)

    return reservation


@router.patch("/patch/{reservation_id}")
async def patch_reservation(reservation_id: int, reservation: ReservationModel):
    log.info(f"Patch reservation: {reservation_id}")

    for r in reservations:
        if r.reservation_id == reservation_id:
            r.name = reservation.name
            r.email = reservation.email
            r.message = reservation.message

            return r

    raise HTTPException(status_code=404, detail="Reservation not found")


@router.delete("/delete/{reservation_id}")
async def delete_reservation(reservation_id: int):
    log.info(f"Delete reservation: {reservation_id}")

    reservation = await get_reservation_by_id(reservation_id)
    if reservation:
        reservations.remove(reservation)
        return reservation

    raise HTTPException(status_code=404, detail="Reservation not found")
