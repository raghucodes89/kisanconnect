from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.crop import Crop
from pydantic import BaseModel

router = APIRouter()

class CropSchema(BaseModel):
    name: str
    category: str
    quantity_kg: float
    price_per_kg: float
    quality: str
    farmer_id: int

@router.post("/")
async def add_crop(data: CropSchema, db: AsyncSession = Depends(get_db)):
    crop = Crop(
        name=data.name,
        category=data.category,
        quantity_kg=data.quantity_kg,
        price_per_kg=data.price_per_kg,
        quality=data.quality,
        farmer_id=data.farmer_id
    )
    db.add(crop)
    await db.commit()
    await db.refresh(crop)
    return {"message": "Crop added successfully", "id": crop.id}

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