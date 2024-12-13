from typing import Type
from sqlalchemy.orm import Session, joinedload

from src.domain.entities.attendance import Attendance
from src.domain.entities.green_angel import GreenAngel
from src.domain.entities.hub import Hub
from src.domain.repository.attendance import IAttendanceRepository


class AttendanceRepository(IAttendanceRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_attendances_paginated(self, page: int, per_page: int, filters: dict = None, order_by: str = 'id', order_direction: str = 'asc') -> dict:
        query = self.db.query(Attendance).options(
            joinedload(Attendance.green_angel),
            joinedload(Attendance.hub),
            joinedload(Attendance.client)
        )

        if filters:
            if 'client_id' in filters and filters['client_id']:
                query = query.filter(Attendance.client_id == filters['client_id'])
            if 'green_angel_id' in filters and filters['green_angel_id']:
                query = query.filter(Attendance.green_angel_id == filters['green_angel_id'])
            if 'green_angel_name' in filters and filters['green_angel_name']:
                query = query.join(Attendance.green_angel).filter(GreenAngel.name.ilike(f"%{filters['green_angel_name']}%"))
            if 'hub_id' in filters and filters['hub_id']:
                query = query.filter(Attendance.hub_id == filters['hub_id'])
            if 'hub_name' in filters and filters['hub_name']:
                query = query.join(Attendance.hub).filter(Hub.name.ilike(f"%{filters['hub_name']}%"))
            if 'attendance_date' in filters and filters['attendance_date']:
                query = query.filter(Attendance.attendance_date == filters['attendance_date'])
            if 'limit_date' in filters and filters['limit_date']:
                query = query.filter(Attendance.limit_date == filters['limit_date'])

        query = query.filter(Attendance.is_active == True)

        allowed_order_by = ['id', 'client_id', 'green_angel_id', 'hub_id', 'limit_date', 'attendance_date', 'is_active', 'created_at', 'updated_at']
        if order_by not in allowed_order_by:
            order_by = 'id'

        if order_direction == 'desc':
            query = query.order_by(getattr(Attendance, order_by).desc())
        else:
            query = query.order_by(getattr(Attendance, order_by))

        total = self.db.query(Attendance).count()
        page = page if page > 0 else 1
        attendances = query.offset((page - 1) * per_page).limit(per_page).all()

        items = []
        for attendance in attendances:
            item = {
                'id': attendance.id,
                'client_id': attendance.client_id,
                'green_angel_id': attendance.green_angel_id,
                'green_angel': {
                    'id': attendance.green_angel.id,
                    'name': attendance.green_angel.name,
                    'is_active': attendance.green_angel.is_active
                },
                'hub_id': attendance.hub_id,
                'hub': {
                    'id': attendance.hub.id,
                    'name': attendance.hub.name,
                    'is_active': attendance.hub.is_active
                },
                'client': {
                    'id': attendance.client.id,
                    'is_active': attendance.client.is_active
                },
                'limit_date': attendance.limit_date,
                'attendance_date': attendance.attendance_date,
                'is_active': attendance.is_active,
                'created_at': attendance.created_at,
                'updated_at': attendance.updated_at
            }
            items.append(item)

        return {
            'size': len(items),
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'items': items
        }

    def find_by_id(self, attendance_id: int) -> Type[Attendance]:
        return self.db.query(Attendance).filter(Attendance.id == attendance_id, Attendance.is_active == True).first()

    def save(self, attendance: Attendance) -> Attendance:
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def delete(self, attendance: Attendance) -> Attendance:
        self.db.delete(attendance)
        self.db.commit()
        return attendance
