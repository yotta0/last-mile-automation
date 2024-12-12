from src.domain.exception.domain_exception import DomainException
from src.domain.exception.error_code import ErrorCode
from src.domain.repository.attendance import IAttendanceRepository
from src.domain.entities.attendance import Attendance
from src.interface.web.schemas.attendance import (
    AttendanceSchema, AttendancesPaginatedSchema, AttendanceUpdateSchema)


class AttendanceService:
    def __init__(self, attendance_repository: IAttendanceRepository):
        self.attendance_repository = attendance_repository

    def get_attendances_paginated(self, page: int, per_page: int) -> dict:
        attendances = self.attendance_repository.get_attendances_paginated(page, per_page)
        return AttendancesPaginatedSchema.model_validate(attendances).model_dump()

    def find_attendance(self, attendance_id: int) -> dict:
        attendance = self.attendance_repository.find_by_id(attendance_id)
        if not attendance:
            raise DomainException(ErrorCode.ATTENDANCE_NOT_FOUND)
        return AttendanceSchema.model_validate(attendance).model_dump()

    def create_attendance(self, attendance_create: AttendanceSchema) -> dict:
        attendance = Attendance(
            client_id=attendance_create.client_id,
            green_angel_id=attendance_create.green_angel_id,
            hub_id=attendance_create.hub_id,
            limit_date=attendance_create.limit_date,
            attendance_date=attendance_create.attendance_date,
            is_active=attendance_create.is_active
        )
        self.attendance_repository.save(attendance)
        return AttendanceSchema.model_validate(attendance).model_dump()

    def update_attendance(self, attendance_id: int, attendance_update: AttendanceUpdateSchema) -> dict:
        attendance = self.attendance_repository.find_by_id(attendance_id)
        if not attendance:
            raise DomainException(ErrorCode.ATTENDANCE_NOT_FOUND)

        if attendance_update.green_angel_id:
            attendance.green_angel_id = attendance_update.green_angel_id
        if attendance_update.hub_id:
            attendance.hub_id = attendance_update.hub_id
        if attendance_update.limit_date:
            attendance.limit_date = attendance_update.limit_date
        if attendance_update.attendance_date:
            attendance.attendance_date = attendance_update.attendance_date
        self.attendance_repository.save(attendance)
        return AttendanceSchema.model_validate(attendance).model_dump()

    def delete_attendance(self, attendance_id: int) -> dict:
        attendance = self.attendance_repository.find_by_id(attendance_id)
        if not attendance:
            raise DomainException(ErrorCode.ATTENDANCE_NOT_FOUND)
        if not attendance.is_active:
            raise DomainException(ErrorCode.ATTENDANCE_ALREADY_DELETED)
        attendance.is_active = False
        self.attendance_repository.save(attendance)
        return AttendanceSchema.model_validate(attendance).model_dump()
