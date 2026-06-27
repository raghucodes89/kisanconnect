from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.crop import Crop
from app.models.farmer import Farmer
from pydantic import BaseModel
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class CropSchema(BaseModel):
    name: str
    category: str
    quantity_kg: float
    price_per_kg: float
    quality: str

async def get_current_farmer(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        farmer_id = int(payload.get("sub"))
        result = await db.execute(select(Farmer).where(Farmer.id == farmer_id))
        farmer = result.scalars().first()
        if not farmer:
            raise HTTPException(status_code=401, detail="Farmer not found")
        return farmer
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/")
async def add_crop(data: CropSchema, db: AsyncSession = Depends(get_db), current_farmer: Farmer = Depends(get_current_farmer)):
    crop = Crop(
        name=data.name,
        category=data.category,
        quantity_kg=data.quantity_kg,
        price_per_kg=data.price_per_kg,
        quality=data.quality,
        farmer_id=current_farmer.id
    )
    db.add(crop)
    await db.commit()
    await db.refresh(crop)
    return {"message": "Crop added successfully", "id": crop.id, "farmer": current_farmer.name}

@router.get("/")
async def get_all_crops(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Crop))
    crops = result.scalars().all()
    return crops

@router.get("/{crop_id}")
async def get_crop(crop_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Crop).where(Crop.id == crop_id))
    crop = result.scalars().first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop

@router.get("/my/crops")
async def get_my_crops(db: AsyncSession = Depends(get_db), current_farmer: Farmer = Depends(get_current_farmer)):
    result = await db.execute(select(Crop).where(Crop.farmer_id == current_farmer.id))
    crops = result.scalars().all()
    return crops