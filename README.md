# 🎟️ Event Booking API

A RESTful API for managing events and user bookings, built with **FastAPI**, **SQLAlchemy**, and **Docker**.

## 🚀 Features

- User registration and JWT authentication
- Event creation and listing
- Ticket booking and management
- PostgreSQL database integration
- Containerized with Docker

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **ORM:** SQLAlchemy
- **Auth:** OAuth2 with JWT
- **Database:** PostgreSQL
- **Containerization:** Docker & Docker Compose

## 📁 Project Structure

```bash
event_booking_API/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── src/
    ├── main.py # FastAPI entrypoint
    ├── models.py # SQLAlchemy models
    ├── schemas.py # Pydantic schemas
    ├── crud.py # DB operations
    ├── auth.py # Authentication logic
    └── database.py # DB engine/session setup
```

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/event_booking_API.git
cd event_booking_API
```

### 2. Set up environment variables

Copy the .env.example and configure:

```bash
cp .env.example .env
```

### 3. Build and run with Docker

```bash
docker-compose up --build
```

The API will be available at http://localhost:8000.

### 4. Access API docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
