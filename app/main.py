from fastapi import FastAPI
from pydantic import BaseModel
from routers import get_locker_time, put_checkin, put_checkout
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime, timedelta
from typing import Optional, Union
from config.database import mongo_connection

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# file based routing
app.include_router(get_locker_time.router)
app.include_router(put_checkout.router)
app.include_router(put_checkin.router)


class Locker(BaseModel):
    locker_id: int
    available: bool
    userId: Optional[str]
    timeIn: Optional[date]
    timeout: Optional[date]
    package: Optional[str]


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.put("/MockTest", status_code=201)
def MockData():
    mockDataList = [
        {
            "locker_id": 1,
            "available": True,
        },
        # late should get at 12.00
        {
            "locker_id": 2,
            "available": False,
            "timeIn": datetime.strptime("2023-02-07T10:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            "timeout": datetime.strptime("2023-02-07T12:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            "userId": 101,
            "package": "Bag",
        },
        {
            "locker_id": 3,
            "available": True,
        },
        # not late
        {
            "locker_id": 4,
            "available": False,
            "timeIn": datetime.strptime("2023-02-03T08:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            "timeout": datetime.strptime("2023-02-08T10:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            "userId": 102,
            "package": "Phone",
        },
        {
            "locker_id": 5,
            "available": True,
        },
        # late
        {
            "locker_id": 6,
            "available": False,
            "timeIn": datetime.strptime("2023-02-04T12:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            "timeout": datetime.strptime("2023-02-07T14:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            "userId": 103,
            "package": "Tablet",
        },
    ]
    mongo_connection["Locker"].insert_many(mockDataList)


@app.put("/Mock", status_code=201)
def MockOneData():
    mockData = {
        "locker_id": 7,
        "available": False,
        "timeIn": datetime.now(),
        "timeout": datetime.now() + timedelta(hours=1),
        "userId": 103,
        "package": "Tablet",
    }
    mongo_connection["Locker"].insert_one(mockData)
