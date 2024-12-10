from typing import Type
from sqlalchemy.orm import Session

from src.domain.entities.attendance import Attendance
from src.domain.repository.attendance import IAttendanceRepository


class AttendanceRepository(IAttendanceRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_attendances_paginated(self, page: int, per_page: int) -> dict:
        total = self.db.query(Attendance).count()
        attendances = self.db.query(Attendance).offset((page - 1) * per_page).limit(per_page).all()
        return {
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'attendances': attendances
        }

    def find_by_id(self, attendance_id: int) -> Type[Attendance]:
        return self.db.query(Attendance).filter(Attendance.id == attendance_id).first()

    def save(self, attendance: Attendance) -> Attendance:
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def delete(self, attendance: Attendance) -> Attendance:
        self.db.delete(attendance)
        self.db.commit()
        return attendance
