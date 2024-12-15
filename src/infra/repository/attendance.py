from typing import Type
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy.sql.expression import desc
from datetime import datetime as dt, timedelta

from workalendar.america import Brazil

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

    def get_sla_metrics(self) -> dict:
        query = self.db.query(Attendance).filter(Attendance.is_active == True)
        total = query.count()
        on_time = query.filter(Attendance.attendance_date <= Attendance.limit_date).count()
        late = total - on_time
        return {
            'total': total,
            'on_time': on_time,
            'late': late,
            'on_time_percentage': round((on_time / total) * 100, 2) if total > 0 else 0,
            'late_percentage': round((late / total) * 100, 2) if total > 0 else 0
        }

    def get_sla_paginated_by_green_angels(self, page: int, per_page: int, filters: dict = None, order_by: str = 'id', order_direction: str = 'asc') -> dict:
        query = self.db.query(
            GreenAngel.id,
            GreenAngel.name,
            func.count(Attendance.id).label('total'),
            func.sum(
                func.cast(Attendance.attendance_date <= Attendance.limit_date, Integer)
            ).label('on_time')
        ).join(Attendance, Attendance.green_angel_id == GreenAngel.id).filter(Attendance.is_active == True)

        if filters:
            if 'green_angel_name' in filters and filters['green_angel_name']:
                query = query.filter(GreenAngel.name.ilike(f"%{filters['green_angel_name']}%"))
            if 'hub_id' in filters and filters['hub_id']:
                query = query.filter(Attendance.hub_id == filters['hub_id'])
            if 'client_id' in filters and filters['client_id']:
                query = query.filter(Attendance.client_id == filters['client_id'])
            if 'attendance_date' in filters and filters['attendance_date']:
                query = query.filter(Attendance.attendance_date == filters['attendance_date'])
            if 'limit_date' in filters and filters['limit_date']:
                query = query.filter(Attendance.limit_date == filters['limit_date'])

        # Group by Green Angel
        query = query.group_by(GreenAngel.id)

        # Sorting logic
        allowed_order_by = ['id', 'name', 'total', 'on_time']
        if order_by not in allowed_order_by:
            order_by = 'id'

        if order_direction == 'desc':
            query = query.order_by(getattr(GreenAngel, order_by).desc())
        else:
            query = query.order_by(getattr(GreenAngel, order_by))

        total = self.db.query(GreenAngel).count()
        page = page if page > 0 else 1
        sla_data = query.offset((page - 1) * per_page).limit(per_page).all()

        items = []
        for result in sla_data:
            green_angel_id = result.id
            total_count = result.total
            on_time = result.on_time
            late = total_count - on_time

            sla_metrics = {
                'green_angel_id': green_angel_id,
                'green_angel_name': result.name,
                'total': total_count,
                'on_time': on_time,
                'late': late,
                'on_time_percentage': round((on_time / total_count) * 100) if total_count > 0 else 0,
                'late_percentage': round((late / total_count) * 100, 2) if total_count > 0 else 0
            }
            items.append(sla_metrics)

        return {
            'size': len(items),
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'items': items
        }

    def find_sla_by_green_angel_id(self, green_angel_id: int) -> dict:
        query = self.db.query(
            GreenAngel.id,
            GreenAngel.name,
            func.count(Attendance.id).label('total'),
            func.sum(
                func.cast(Attendance.attendance_date <= Attendance.limit_date, Integer)
            ).label('on_time')
        ).join(Attendance, Attendance.green_angel_id == GreenAngel.id).filter(GreenAngel.id == green_angel_id).filter(Attendance.is_active == True).group_by(GreenAngel.id).first()

        if not query:
            return None

        total_count = query.total
        on_time = query.on_time
        late = total_count - on_time

        return {
            'green_angel_id': query.id,
            'green_angel_name': query.name,
            'total': total_count,
            'on_time': on_time,
            'late': late,
            'on_time_percentage': round((on_time / total_count) * 100) if total_count > 0 else 0,
            'late_percentage': round((late / total_count) * 100, 2) if total_count > 0 else 0
        }

    def get_sla_paginated_by_hubs(self, page: int, per_page: int, filters: dict = None, order_by: str = 'id', order_direction: str = 'asc') -> dict:
        query = self.db.query(
            Hub.id,
            Hub.name,
            func.count(Attendance.id).label('total'),
            func.sum(
                func.cast(Attendance.attendance_date <= Attendance.limit_date, Integer)
            ).label('on_time')
        ).join(Attendance, Attendance.hub_id == Hub.id).filter(Attendance.is_active == True)

        if filters:
            if 'hub_name' in filters and filters['hub_name']:
                query = query.filter(Hub.name.ilike(f"%{filters['hub_name']}%"))
            if 'green_angel_id' in filters and filters['green_angel_id']:
                query = query.filter(Attendance.green_angel_id == filters['green_angel_id'])
            if 'client_id' in filters and filters['client_id']:
                query = query.filter(Attendance.client_id == filters['client_id'])
            if 'attendance_date' in filters and filters['attendance_date']:
                query = query.filter(Attendance.attendance_date == filters['attendance_date'])
            if 'limit_date' in filters and filters['limit_date']:
                query = query.filter(Attendance.limit_date == filters['limit_date'])

        # Group by Hub
        query = query.group_by(Hub.id)

        # Sorting logic
        allowed_order_by = ['id', 'name', 'total', 'on_time']
        if order_by not in allowed_order_by:
            order_by = 'id'

        if order_direction == 'desc':
            query = query.order_by(getattr(Hub, order_by).desc())
        else:
            query = query.order_by(getattr(Hub, order_by))

        total = self.db.query(Hub).count()
        page = page if page > 0 else 1
        sla_data = query.offset((page - 1) * per_page).limit(per_page).all()

        items = []
        for result in sla_data:
            hub_id = result.id
            total_count = result.total
            on_time = result.on_time
            late = total_count - on_time

            sla_metrics = {
                'hub_id': hub_id,
                'hub_name': result.name,
                'total': total_count,
                'on_time': on_time,
                'late': late,
                'on_time_percentage': round((on_time / total_count) * 100) if total_count > 0 else 0,
                'late_percentage': round((late / total_count) * 100, 2) if total_count > 0 else 0
            }
            items.append(sla_metrics)

        return {
            'size': len(items),
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'items': items
        }

    def find_sla_by_hub_id(self, hub_id: int) -> dict:
        query = self.db.query(
            Hub.id,
            Hub.name,
            func.count(Attendance.id).label('total'),
            func.sum(
                func.cast(Attendance.attendance_date <= Attendance.limit_date, Integer)
            ).label('on_time')
        ).join(Attendance, Attendance.hub_id == Hub.id).filter(Hub.id == hub_id).filter(Attendance.is_active == True).group_by(Hub.id).first()

        if not query:
            return None

        total_count = query.total
        on_time = query.on_time
        late = total_count - on_time

        return {
            'hub_id': query.id,
            'hub_name': query.name,
            'total': total_count,
            'on_time': on_time,
            'late': late,
            'on_time_percentage': round((on_time / total_count) * 100) if total_count > 0 else 0,
            'late_percentage': round((late / total_count) * 100, 2) if total_count > 0 else 0
        }

    def get_productivity_paginated(self, page: int, per_page: int, filters: dict = None, order_by: str = 'total_attendances', order_direction: str = 'desc') -> dict:

        calendar = Brazil()

        # Base query
        query = self.db.query(
            Attendance.green_angel_id,
            func.count(Attendance.id).label('total_attendances')
        ).filter(Attendance.attendance_date.isnot(None)).filter(Attendance.is_active == True)

        if filters.get('date_from'):
            date_from = dt.strptime(filters['date_from'], '%Y-%m-%d %H:%M:%S')
            query = query.filter(Attendance.attendance_date >= date_from)
        else:
            date_from = None

        if filters.get('date_to'):
            date_to = dt.strptime(filters['date_to'], '%Y-%m-%d %H:%M:%S')
            query = query.filter(Attendance.attendance_date <= date_to)
        else:
            date_to = dt.today()

        if date_from:
            working_days = sum(1 for d in (date_from + timedelta(n) for n in range((date_to - date_from).days + 1))
                               if calendar.is_working_day(d))
        else:
            working_days = 1

        query = query.group_by(Attendance.green_angel_id)

        allowed_order_by = ['total_attendances']
        if order_by not in allowed_order_by:
            order_by = 'total_attendances'

        if order_by == 'total_attendances' and order_direction == 'desc':
            query = query.order_by(desc('total_attendances'))
        elif order_by == 'total_attendances':
            query = query.order_by('total_attendances')

        total = query.count()
        sla_data = query.offset((page - 1) * per_page).limit(per_page).all()

        items = []
        for result in sla_data:
            productivity = result.total_attendances / working_days if working_days > 0 else 0
            items.append({
                'green_angel_id': result.green_angel_id,
                'total_attendances': result.total_attendances,
                'working_days': working_days,
                'attendances_per_day': round(productivity, 2)
            })

        return {
            'size': len(items),
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'items': items
        }

    def _calculate_working_days(self, date_from: str, date_to: str) -> int:
        from datetime import datetime, timedelta

        start_date = datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S')

        num_working_days = 0
        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() < 5:  # Monday to Friday are working days
                num_working_days += 1
            current_date += timedelta(days=1)

        return num_working_days
