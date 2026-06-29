from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.transport import Transport
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class TransportSchema(BaseModel):
    owner_name: str
    phone: str
    vehicle_type: str
    vehicle_number: str
    capacity_tons: float
    from_location: str
    to_location: str
    cost_per_km: float
    district: str
    state: str

@router.post("/register")
async def register_transport(data: TransportSchema, db: AsyncSession = Depends(get_db)):
    transport = Transport(
        owner_name=data.owner_name,
        phone=data.phone,
        vehicle_type=data.vehicle_type,
        vehicle_number=data.vehicle_number,
        capacity_tons=data.capacity_tons,
        from_location=data.from_location,
        to_location=data.to_location,
        cost_per_km=data.cost_per_km,
        district=data.district,
        state=data.state
    )
    db.add(transport)
    await db.commit()
    await db.refresh(transport)
    return {"message": "Transport registered successfully", "id": transport.id}

@router.get("/")
async def get_all_transport(
    vehicle_type: Optional[str] = None,
    from_location: Optional[str] = None,
    district: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Transport).where(Transport.availability == "available"))
    vehicles = result.scalars().all()

    if vehicle_type:
        vehicles = [v for v in vehicles if v.vehicle_type.lower() == vehicle_type.lower()]
    if from_location:
        vehicles = [v for v in vehicles if from_location.lower() in v.from_location.lower()]
    if district:
        vehicles = [v for v in vehicles if v.district.lower() == district.lower()]

    return vehicles

@router.get("/{transport_id}")
async def get_transport(transport_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Transport).where(Transport.id == transport_id))
    vehicle = result.scalars().first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Transport not found")
    return vehicle

@router.patch("/{transport_id}/availability")
async def update_availability(
    transport_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Transport).where(Transport.id == transport_id))
    vehicle = result.scalars().first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Transport not found")
    vehicle.availability = "busy" if vehicle.availability == "available" else "available"
    await db.commit()
    return {"message": f"Availability updated to {vehicle.availability}"}

@router.get("/vehicle-types/list")
async def get_vehicle_types():
    return {
        "vehicle_types": [
            "Truck",
            "Mini Truck",
            "Tractor",
            "Tempo",
            "Pickup Van",
            "Container Truck"
        ]
    }