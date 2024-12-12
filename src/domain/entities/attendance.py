from sqlalchemy import Integer, Column, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime as dt

from src.domain.entities.green_angel import GreenAngel
from src.domain.entities.client import Client
from src.domain.entities.hub import Hub

from src.infra.database.database import Base

class Attendance(Base):
    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    green_angel_id = Column(Integer, ForeignKey('green_angels.id'), nullable=False)
    hub_id = Column(Integer, ForeignKey('hubs.id'), nullable=False)
    limit_date = Column(DateTime, nullable=False)
    attendance_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow)

    green_angel = relationship('GreenAngel', back_populates='attendances')
    hub = relationship('Hub', back_populates='attendances')
    client = relationship('Client', back_populates='attendances')
