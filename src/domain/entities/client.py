from sqlalchemy import Integer, Column, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime as dt

from src.infra.database.database import Base

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow)

    attendances = relationship('Attendance', back_populates='client')
