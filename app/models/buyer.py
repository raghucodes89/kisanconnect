from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Buyer(Base):
    __tablename__ = "buyers"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False)
    phone        = Column(String, nullable=False)
    email        = Column(String, unique=True, nullable=False)
    password     = Column(String, nullable=False)
    buyer_type   = Column(String)  # local, exporter, importer, wholesaler
    company_name = Column(String)
    city         = Column(String)
    state        = Column(String)
    is_verified  = Column(Boolean, default=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())