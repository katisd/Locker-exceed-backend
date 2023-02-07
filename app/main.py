from fastapi import FastAPI
from pydantic import BaseModel
from routers import get_locker_time, put_checkin, put_checkout
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime
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
    timeIn: Optional[datetime]
    timeout: Optional[datetime]
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
        {
            "locker_id": 2,
            "available": False,
            "timeIn": "2021-01-02T10:00:00Z",
            "timeout": "2021-01-02T12:00:00Z",
            "userId": "101",
            "package": "Bag",
        },
        {
            "locker_id": 3,
            "available": True,
        },
        {
            "locker_id": 4,
            "available": False,
            "timeIn": "2021-01-03T08:00:00Z",
            "timeout": "2021-01-03T10:00:00Z",
            "userId": "102",
            "package": "Phone",
        },
        {
            "locker_id": 5,
            "available": True,
        },
        {
            "locker_id": 6,
            "available": False,
            "timeIn": "2021-01-04T12:00:00Z",
            "timeout": "2021-01-04T14:00:00Z",
            "userId": "103",
            "package": "Tablet",
        },
    ]
    mongo_connection["Locker"].insert_many(mockDataList)
