from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import models, schemas
from auth import get_password_hash
import datetime


async def get_user_by_email(db: AsyncSession, email: EmailStr):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, password_hash=hashed_password, name=user.name, created_at=datetime.datetime.now())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_events(db: AsyncSession):
    result = await db.execute(select(models.Event))
    return result.scalars().all()


async def create_user_event(db: AsyncSession, event: schemas.EventCreate, user_id: int):
    db_event = models.Event(**event.model_dump(), owner_id=user_id)
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    return db_event


async def get_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(models.Event).filter(models.Event.id == event_id))
    return result.scalar_one_or_none()


async def get_bookings_for_event(db: AsyncSession, event_id: int):
    result = await db.execute(select(models.Booking).filter(models.Booking.event_id == event_id))
    return result.scalars().all()


async def get_total_booked_seats_for_event(db: AsyncSession, event_id: int):
    result = await db.execute(
        select(func.sum(models.Booking.seats_booked)).filter(models.Booking.event_id == event_id)
    )
    total_seats = result.scalar_one_or_none()
    return total_seats if total_seats is not None else 0


async def get_booking_by_user_and_event(db: AsyncSession, user_id: int, event_id: int):
    result = await db.execute(
        select(models.Booking).filter(
            models.Booking.user_id == user_id,
            models.Booking.event_id == event_id
        )
    )
    return result.scalar_one_or_none()


async def create_booking(db: AsyncSession, booking: schemas.BookingCreate, user_id: int, event_id: int):
    db_booking = models.Booking(**booking.model_dump(), user_id=user_id, event_id=event_id)
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking


async def get_user_events(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Event).filter(models.Event.owner_id == user_id))
    return result.scalars().all()


async def get_user_bookings(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Booking).filter(models.Booking.user_id == user_id))
    return result.scalars().all()
