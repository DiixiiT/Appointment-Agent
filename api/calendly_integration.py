from datetime import date, datetime
from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AppointmentType(str, Enum):
    consultation = "consultation"
    followup = "followup"
    physical = "physical"
    special = "special"


class Patient(BaseModel):
    name: str
    email: str
    phone: str


class Book(BaseModel):
    appointment_type: AppointmentType
    date: date
    start_time: datetime
    patient: Patient
    reason: str


@router.get("/availability")
async def get_availablity_data(date_param: date):
    return {
        "date": "2025-11-15",
        "availability_solts": [
            {"start_time": "9:00", "end_time": "9:30", "availability": True},
            {"start_time": "9:30", "end_time": "10:00", "availability": False},
            {"start_time": "10:30", "end_time": "11:00", "availability": True},
        ],
    }


@router.post("/book")
async def book(book_in: Book):
    print(
        book_in,
        "Done with  booking ********************************************************",
    )
    return {
        "booking_id": "AAA-123-1",
        "status": "confirmed",
        "confirmation_code": "1234",
        "details": "Success",
        "booked_data": book_in,
    }
