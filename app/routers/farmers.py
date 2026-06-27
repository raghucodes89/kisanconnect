from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.farmer import Farmer

router = APIRouter()

@router.get("/")
async def get_all_farmers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Farmer))
    farmers = result.scalars().all()
    return farmers

@router.get("/{farmer_id}")
async def get_farmer(farmer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Farmer).where(Farmer.id == farmer_id))
    farmer = result.scalars().first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer