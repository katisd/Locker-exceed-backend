from fastapi import APIRouter, Body
from config.database import mongo_connection
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Union

router = APIRouter(
    prefix="/checkin",
    tags=["checkin"],
    responses={404: {"description": "Not found"}},
)


class Locker(BaseModel):
    locker_id: int
    available: bool
    userId: Optional[str]
    timeIn: Optional[datetime]
    timeout: Optional[datetime]
    package: Optional[str]


@router.put("/")
def get_reservation_locker(userId: str = Body(), timeout: datetime = Body(), package:str = Body()):
    timeIn = datetime.now()
    locker = mongo_connection["Locker"].find_one({"available": True}, {'_id': False})
    if timeIn.timestamp() > timeout.timestamp():
        return {"error": "inappropriate time"}
    elif package == "":
        return {"error": "Put some item in"}
    elif locker is None:
        return {"error": "Locker is not available"}
    else:
        timeout_timestamp = datetime.timestamp(timeout)
        timeIn_timestamp = datetime.timestamp(timeIn)
        diff = int((timeout_timestamp - timeIn_timestamp) // 3600)
        cost = 0
        if diff > 2:
            cost = (diff - 2) * 5
        mongo_connection["Locker"].update_one(
            {"available": True},
            {"$set": {
                "available": False,
                "userId": userId,
                "timeIn": timeIn,
                "timeout": timeout,
                "package": package,
            }
            }
        )
        return {"message": "Locker successfully reserved", "cost": cost, "locker_id": locker["locker_id"]}
