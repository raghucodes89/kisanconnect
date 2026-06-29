from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.buyer import Buyer
from app.models.crop import Crop
from app.models.farmer import Farmer
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class BuyerRegisterSchema(BaseModel):
    name: str
    phone: str
    email: str
    password: str
    buyer_type: str
    company_name: str
    city: str
    state: str

class BuyerLoginSchema(BaseModel):
    email: str
    password: str

class EnquirySchema(BaseModel):
    crop_id: int
    buyer_id: int
    message: str
    offered_price: float
    quantity_needed: float

@router.post("/register")
async def register_buyer(data: BuyerRegisterSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Buyer).where(Buyer.email == data.email))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    buyer = Buyer(
        name=data.name,
        phone=data.phone,
        email=data.email,
        password=pwd_context.hash(data.password),
        buyer_type=data.buyer_type,
        company_name=data.company_name,
        city=data.city,
        state=data.state
    )
    db.add(buyer)
    await db.commit()
    await db.refresh(buyer)
    return {"message": "Buyer registered successfully", "id": buyer.id}

@router.post("/login")
async def login_buyer(data: BuyerLoginSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Buyer).where(Buyer.email == data.email))
    buyer = result.scalars().first()
    if not buyer or not pwd_context.verify(data.password, buyer.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful", "buyer_id": buyer.id, "name": buyer.name}

@router.get("/")
async def get_all_buyers(
    buyer_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Buyer))
    buyers = result.scalars().all()
    if buyer_type:
        buyers = [b for b in buyers if b.buyer_type.lower() == buyer_type.lower()]
    return [
        {
            "id": b.id,
            "name": b.name,
            "company_name": b.company_name,
            "buyer_type": b.buyer_type,
            "city": b.city,
            "state": b.state,
            "phone": b.phone
        }
        for b in buyers
    ]

@router.get("/{buyer_id}")
async def get_buyer(buyer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Buyer).where(Buyer.id == buyer_id))
    buyer = result.scalars().first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return buyer

@router.get("/browse/crops")
async def browse_crops_as_buyer(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Crop).where(Crop.status == "available"))
    crops = result.scalars().all()
    if category:
        crops = [c for c in crops if c.category.lower() == category.lower()]
    if max_price:
        crops = [c for c in crops if c.price_per_kg <= max_price]
    response = []
    for c in crops:
        farmer_result = await db.execute(select(Farmer).where(Farmer.id == c.farmer_id))
        farmer = farmer_result.scalars().first()
        response.append({
            "crop_id": c.id,
            "crop_name": c.name,
            "category": c.category,
            "quantity_kg": c.quantity_kg,
            "price_per_kg": c.price_per_kg,
            "quality": c.quality,
            "farmer_name": farmer.name if farmer else "Unknown",
            "farmer_phone": farmer.phone if farmer else "Unknown",
            "farmer_village": farmer.village if farmer else "Unknown",
            "whatsapp_link": f"https://wa.me/91{farmer.phone}?text=Hi%20{farmer.name},%20I%20am%20interested%20in%20buying%20your%20{c.name}" if farmer else None
        })
    return response

@router.get("/types/list")
async def get_buyer_types():
    return {
        "buyer_types": [
            "Local Buyer",
            "Wholesaler",
            "Retailer",
            "Exporter",
            "Importer",
            "Food Processor",
            "Restaurant",
            "Hotel"
        ]
    }