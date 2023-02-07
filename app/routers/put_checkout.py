from fastapi import APIRouter, HTTPException, Body
from typing import Union, Optional
from pydantic import BaseModel
from datetime import date, datetime
from config.database import mongo_connection
from math import ceil


router = APIRouter(
    prefix="/checkout",
    tags=["checkout"],
    responses={404: {"description": "Not found"}},
)

class Locker(BaseModel):
    locker_id: int
    available: bool
    userId: Optional[str]
    timeIn: Optional[datetime]
    timeout: Optional[datetime]
    package: Optional[str]

@router.get("/{userId}/{locker_id}")                    #คิดค่าใช้จ่ายอย่างเดียว
def check_out_price(userId: str,locker_id: int):
    data = mongo_connection["Locker"].find_one({"userId": userId,"locker_id": locker_id},{"_id":False})
    moreexcess = 0
    price = 0
    if not data:
        raise HTTPException(400, detail="No UserId or LockerId in database")
    moreexcess = datetime.now().timestamp() - dict(data)["timeout"].timestamp()
    if moreexcess > 0:
        price += ceil(abs(moreexcess)/600)*20
    return price

@router.put("/{userId}/{locker_id}/{money}")            #คิดค่าใช้จ่ายและเงินทอนโดยแสดงค่าเงินทอนออกมา สุดท้ายถ้าเงินที่จ่ายเพียงพอจะ update status ใน database
def check_out_price(userId: str,money: int,locker_id: int):
    data = mongo_connection["Locker"].find_one({"userId": userId,"locker_id": locker_id},{"_id":False})
    moreexcess = 0
    price = 0
    change = 0
    if not data:
        raise HTTPException(400, detail="No UserId or LockerId in database")
    moreexcess = datetime.now().timestamp() - dict(data)["timeout"].timestamp()
    if moreexcess > 0:
        price += ceil(abs(moreexcess)/600)*20
    change = money - price
    if change < 0:
        raise HTTPException(400, detail="Insufficient fund")
    mongo_connection["Locker"].update_one({"userId": userId},{"$set": {"available": True}})
    mongo_connection["Locker"].update_one({"userId": userId},{"$unset": {"userId": "", "timeIn": "", "timeout": "", "package": ""}})
    return change