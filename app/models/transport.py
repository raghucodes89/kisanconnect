from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Transport(Base):
    __tablename__ = "transport"

    id              = Column(Integer, primary_key=True, index=True)
    owner_name      = Column(String, nullable=False)
    phone           = Column(String, nullable=False)
    vehicle_type    = Column(String)  # truck, mini truck, tractor, tempo
    vehicle_number  = Column(String)
    capacity_tons   = Column(Float)
    from_location   = Column(String)
    to_location     = Column(String)
    cost_per_km     = Column(Float)
    availability    = Column(String, default="available")
    district        = Column(String)
    state           = Column(String, default="Andhra Pradesh")
    created_at      = Column(DateTime(timezone=True), server_default=func.now())