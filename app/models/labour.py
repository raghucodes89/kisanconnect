from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Labour(Base):
    __tablename__ = "labour"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False)
    phone        = Column(String, nullable=False)
    village      = Column(String)
    district     = Column(String)
    state        = Column(String, default="Andhra Pradesh")
    skill        = Column(String)  # ploughing, harvesting, planting, spraying
    daily_wage   = Column(Float)
    availability = Column(String, default="available")  # available, busy
    experience_years = Column(Integer, default=0)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())