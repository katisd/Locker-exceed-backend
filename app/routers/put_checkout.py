from fastapi import APIRouter, Body


router = APIRouter(
    prefix="/checkout",
    tags=["checkout"],
    responses={404: {"description": "Not found"}},
)
