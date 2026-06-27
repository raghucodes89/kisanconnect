from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Crop(Base):
    __tablename__ = "crops"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    category    = Column(String)
    quantity_kg = Column(Float)
    price_per_kg= Column(Float)
    quality     = Column(String)
    status      = Column(String, default="available")
    farmer_id   = Column(Integer, ForeignKey("farmers.id"))
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    farmer      = relationship("Farmer", back_populates="crops")