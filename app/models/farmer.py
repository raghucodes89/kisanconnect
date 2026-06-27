from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
class Farmer(Base):
    __tablename__ = "farmers"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    phone      = Column(String, unique=True, nullable=False)
    email      = Column(String, unique=True, nullable=False)
    password   = Column(String, nullable=False)
    village    = Column(String)
    district   = Column(String)
    state      = Column(String, default="Andhra Pradesh")
    land_acres = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    crops      = relationship("Crop", back_populates="farmer")