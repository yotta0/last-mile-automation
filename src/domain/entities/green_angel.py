from sqlalchemy import Integer, Column, String, Boolean, DateTime
from datetime import datetime as dt

from sqlalchemy.orm import relationship

from src.infra.database.database import Base

class GreenAngel(Base):
    __tablename__ = 'green_angels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False, unique=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow)

    attendances = relationship('Attendance', back_populates='green_angel')
