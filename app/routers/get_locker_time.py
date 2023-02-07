from fastapi import APIRouter, Body
from typing import Union, Optional
from pydantic import BaseModel
from config.database import mongo_connection

router = APIRouter(
    prefix="/lockers",
    tags=["lockers"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def lockers():
    return {"msg": "order"}
