# KisanConnect API

AgriTech platform for Indian farmers built with FastAPI and PostgreSQL.

## Features
- Farmer registration and JWT authentication
- Crop management (add, browse, search)
- Live weather advisory with farming advice
- Marketplace for buyers to browse crops

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- JWT Authentication
- OpenWeatherMap API
- Redis (coming soon)

## API Endpoints
- POST /auth/register — register farmer
- POST /auth/login — login and get JWT token
- POST /crops/ — add crop (protected)
- GET /crops/ — list all crops
- GET /weather/{city} — weather + farming advice
- GET /marketplace/crops — buyers browse crops
- GET /marketplace/search — search crops by name

## Setup
1. Clone the repo
2. Install dependencies: pip install -r requirements.txt
3. Set up .env file with DATABASE_URL and SECRET_KEY
4. Run: uvicorn main:app --reload