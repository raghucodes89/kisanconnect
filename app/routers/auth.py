from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.database import get_db
from app.models.farmer import Farmer
from app.config import settings
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterSchema(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    village: str
    district: str
    state: str
    land_acres: float

class LoginSchema(BaseModel):
    email: str
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@router.post("/register")
async def register(data: RegisterSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Farmer).where(Farmer.email == data.email))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    farmer = Farmer(
        name=data.name,
        phone=data.phone,
        email=data.email,
        password=hash_password(data.password),
        village=data.village,
        district=data.district,
        state=data.state,
        land_acres=data.land_acres
    )
    db.add(farmer)
    await db.commit()
    await db.refresh(farmer)
    return {"message": "Farmer registered successfully", "id": farmer.id}

@router.post("/login")
async def login(data: LoginSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Farmer).where(Farmer.email == data.email))
    farmer = result.scalars().first()
    if not farmer or not verify_password(data.password, farmer.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token({"sub": str(farmer.id), "email": farmer.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Farmer).where(Farmer.email == form_data.username))
    farmer = result.scalars().first()
    if not farmer or not verify_password(form_data.password, farmer.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_token({"sub": str(farmer.id), "email": farmer.email})
    return {"access_token": access_token, "token_type": "bearer"}