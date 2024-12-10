from src.interface.web.schemas.attendance import AttendanceCreateSchema, AttendanceSchema
from src.application.service.attendance import AttendanceService


class AttendanceController:
    def __init__(self, attendance_service: AttendanceService):
        self.attendance_service = attendance_service

    def get_attendances(self, page: int, per_page: int) -> dict:
        return self.attendance_service.get_attendances_paginated(page, per_page)

    def get_attendance(self, attendance_id: int) -> dict:
        return self.attendance_service.find_attendance(attendance_id)

    def create_attendance(self, attendance_create: AttendanceCreateSchema) -> dict:
        return self.attendance_service.create_attendance(attendance_create)

    def update_attendance(self, attendance_id: int, attendance_update: AttendanceSchema) -> dict:
        return self.attendance_service.update_attendance(attendance_id, attendance_update)

    def delete_attendance(self, attendance_id: int) -> dict:
        return self.attendance_service.delete_attendance(attendance_id)
