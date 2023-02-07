from fastapi import APIRouter, Body

router = APIRouter(
    prefix="/checkin",
    tags=["checkin"],
    responses={404: {"description": "Not found"}},
)
