from fastapi import FastAPI
from pydantic import BaseModel
from routers import get_locker_time, put_checkin, put_checkout
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime
from typing import Optional, Union

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
    locker_status: str
    userId: Optional[str]
    timeIn: Optional[date]
    timeout: Optional[date]
    package: Optional[str]


@app.get("/")
def root():
    return {"message": "Hello World"}
