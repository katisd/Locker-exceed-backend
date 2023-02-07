from fastapi import APIRouter, Body
from typing import Union, Optional
from pydantic import BaseModel
from datetime import date, datetime
from config.database import mongo_connection

router = APIRouter(
    prefix="/lockers",
    tags=["lockers"],
    responses={404: {"description": "Not found"}},
)

# this endpont return list of lockers
# 1. if locker is available, return id and status
# 2. if locker is not available, return time left in minutes
# 2.1 if time left is negative (User late to get package), return None
# 2.2 if time left is positive (User still have time to get package), return time left in minutes
@router.get("/")
def lockers():
    data = list(mongo_connection["Locker"].find({}, {"_id": False}))
    res = []

    def timeLeft(timeout):
        now = datetime.now()
        # if not late return known time
        if now > timeout:
            timeLeft = now - timeout
            return timeLeft.total_seconds() // 60
        # if late return None
        else:
            return None

    for record in data:
        if record["available"] == True:
            res.append(record)
        else:
            tmp = {
                "locker_id": record["locker_id"],
                "available": record["available"],
                # # these data is not needed for frontend
                # "timeIn": record["timeIn"],
                # "timeout": record["timeout"],
                # "userId": record["userId"],
                # "package": record["package"],
                "timeLeft": timeLeft(record["timeout"]),
            }
            res.append(tmp)
    return list(res)
