from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    name: str

class UserInDB(UserBase):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class EventBase(BaseModel):
    title: str
    description: str
    datetime: datetime
    max_seats: int

class EventCreate(EventBase):
    pass

class EventInDB(EventBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    seats_booked: int

class BookingCreate(BookingBase):
    pass

class BookingInDB(BookingBase):
    id: int
    user_id: int
    event_id: int

    class Config:
        from_attributes = True