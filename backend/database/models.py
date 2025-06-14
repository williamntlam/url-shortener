from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class URLModel(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    original_url = Column(String(2048), nullable=False)
    short_code = Column(String(10), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    clicks = Column(Integer, default=0)
    is_expired = Column(Boolean, default=False)
    expiry_date = Column(DateTime, nullable=True)
    is_one_time = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True) 