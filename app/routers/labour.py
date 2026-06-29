from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.labour import Labour
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class LabourSchema(BaseModel):
    name: str
    phone: str
    village: str
    district: str
    state: str
    skill: str
    daily_wage: float
    experience_years: int

class LabourUpdateSchema(BaseModel):
    availability: str

@router.post("/register")
async def register_labour(data: LabourSchema, db: AsyncSession = Depends(get_db)):
    labour = Labour(
        name=data.name,
        phone=data.phone,
        village=data.village,
        district=data.district,
        state=data.state,
        skill=data.skill,
        daily_wage=data.daily_wage,
        experience_years=data.experience_years
    )
    db.add(labour)
    await db.commit()
    await db.refresh(labour)
    return {"message": "Labour registered successfully", "id": labour.id}

@router.get("/")
async def get_all_labour(
    skill: Optional[str] = None,
    district: Optional[str] = None,
    max_wage: Optional[float] = None,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Labour).where(Labour.availability == "available"))
    workers = result.scalars().all()

    if skill:
        workers = [w for w in workers if w.skill.lower() == skill.lower()]
    if district:
        workers = [w for w in workers if w.district.lower() == district.lower()]
    if max_wage:
        workers = [w for w in workers if w.daily_wage <= max_wage]

    return workers

@router.get("/{labour_id}")
async def get_labour(labour_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Labour).where(Labour.id == labour_id))
    worker = result.scalars().first()
    if not worker:
        raise HTTPException(status_code=404, detail="Labour not found")
    return worker

@router.patch("/{labour_id}/availability")
async def update_availability(
    labour_id: int,
    data: LabourUpdateSchema,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Labour).where(Labour.id == labour_id))
    worker = result.scalars().first()
    if not worker:
        raise HTTPException(status_code=404, detail="Labour not found")
    worker.availability = data.availability
    await db.commit()
    return {"message": f"Availability updated to {data.availability}"}

@router.get("/skills/list")
async def get_skills():
    return {
        "skills": [
            "Ploughing",
            "Harvesting",
            "Planting",
            "Spraying",
            "Irrigation",
            "Weeding",
            "Transplanting",
            "Sorting",
            "Packing",
            "Driving Tractor"
        ]
    }