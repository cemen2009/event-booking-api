from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, init_db
import schemas, crud, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Event Booking API",
    description="A REST API for managing events and bookings with FastAPI and PostgreSQL.",
    version="1.0",
    lifespan=lifespan
)


@app.post("/register", response_model=schemas.UserInDB, summary="Register a new user")
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await crud.create_user(db=db, user=user)


@app.post("/login", response_model=schemas.Token, summary="Login into the system and obtain a JWT token")
async def login_for_access_token(user: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)

    if not db_user or not auth.verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_toke(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/events", response_model=list[schemas.EventInDB], summary="Get list of all events")
async def read_events(
        db: AsyncSession = Depends(get_db),
        current_user: schemas.UserInDB = Depends(auth.get_current_user)
):
    events = await crud.get_events(db)
    return events


@app.post(
    "/events",
    response_model=schemas.EventInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new event"
)
async def create_event(
        event: schemas.EventCreate,
        db: AsyncSession = Depends(get_db),
        current_user: schemas.UserInDB = Depends(auth.get_current_user)
):
    return await crud.create_user_event(db=db, event=event, user_id=current_user.id)


@app.post("/events/{event_id}/book", response_model=schemas.BookingInDB, summary="Book an event")
async def book_event(
        event_id: int,
        booking: schemas.BookingCreate,
        db: AsyncSession = Depends(get_db),
        current_user: schemas.UserInDB = Depends(auth.get_current_user)
):
    db_event = await crud.get_event(db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="An event does not exist")

    existing_booking = await crud.get_booking_by_user_and_event(
        db,
        user_id=current_user.id,
        event_id=event_id
    )
    if existing_booking is not None:
        raise HTTPException(status_code=400, detail="Booking already exists")

    total_booked_seats = await crud.get_total_booked_seats_for_event(
        db,
        event_id=event_id
    )
    available_seats = db_event.max_seats - total_booked_seats

    if booking.seats_booked <= 0:
        raise HTTPException(status_code=400, detail="Amount of booked seats cannot be negative")

    if booking.seats_booked > available_seats:
        raise HTTPException(
            status_code=400,
            detail=f"Amount of booked seats cannot be greater than available seats. "
                   f"Available amount of seats: {available_seats}"
        )

    return await crud.create_booking(db=db, booking=booking, user_id=current_user.id, event_id=event_id)


@app.get("/my/events", response_model=list[schemas.EventInDB], summary="Get all events of current user")
async def get_my_events(
        db: AsyncSession = Depends(get_db),
        current_user: schemas.UserInDB = Depends(auth.get_current_user)
):
    return await crud.get_user_events(db=db, user_id=current_user.id)


@app.get("/my/booking", response_model=list[schemas.BookingInDB], summary="Get all bookings of current user")
async def get_my_bookings(
        db: AsyncSession = Depends(get_db),
        current_user: schemas.UserInDB = Depends(auth.get_current_user)
):
    return await crud.get_user_bookings(db=db, user_id=current_user.id)
