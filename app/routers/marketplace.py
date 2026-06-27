from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.crop import Crop
from app.models.farmer import Farmer
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class BidSchema(BaseModel):
    crop_id: int
    buyer_name: str
    buyer_phone: str
    offer_price_per_kg: float
    quantity_kg: float

@router.get("/crops")
async def browse_crops(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    quality: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Crop).where(Crop.status == "available")
    result = await db.execute(query)
    crops = result.scalars().all()

    if category:
        crops = [c for c in crops if c.category.lower() == category.lower()]
    if max_price:
        crops = [c for c in crops if c.price_per_kg <= max_price]
    if quality:
        crops = [c for c in crops if c.quality.lower() == quality.lower()]

    return [
        {
            "id": c.id,
            "name": c.name,
            "category": c.category,
            "quantity_kg": c.quantity_kg,
            "price_per_kg": c.price_per_kg,
            "quality": c.quality,
            "farmer_id": c.farmer_id
        }
        for c in crops
    ]

@router.get("/crops/{crop_id}")
async def get_crop_detail(crop_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Crop).where(Crop.id == crop_id))
    crop = result.scalars().first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")

    farmer_result = await db.execute(select(Farmer).where(Farmer.id == crop.farmer_id))
    farmer = farmer_result.scalars().first()

    return {
        "crop_id": crop.id,
        "name": crop.name,
        "category": crop.category,
        "quantity_kg": crop.quantity_kg,
        "price_per_kg": crop.price_per_kg,
        "quality": crop.quality,
        "status": crop.status,
        "farmer_name": farmer.name if farmer else "Unknown",
        "farmer_phone": farmer.phone if farmer else "Unknown",
        "farmer_village": farmer.village if farmer else "Unknown",
        "farmer_district": farmer.district if farmer else "Unknown"
    }

@router.get("/search")
async def search_crops(q: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Crop).where(Crop.status == "available"))
    crops = result.scalars().all()
    filtered = [c for c in crops if q.lower() in c.name.lower()]
    return filtered