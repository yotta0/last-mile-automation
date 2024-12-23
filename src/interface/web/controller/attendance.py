from src.interface.web.schemas.attendance import AttendanceCreateSchema, AttendanceSchema
from src.application.service.attendance import AttendanceService


class AttendanceController:
    def __init__(self, attendance_service: AttendanceService):
        self.attendance_service = attendance_service

    def get_attendances(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        return self.attendance_service.get_attendances_paginated(page, per_page, filters, order_by, order_direction)

    def get_attendance(self, attendance_id: int) -> dict:
        return self.attendance_service.find_attendance(attendance_id)

    def create_attendance(self, attendance_create: AttendanceCreateSchema) -> dict:
        return self.attendance_service.create_attendance(attendance_create)

    def update_attendance(self, attendance_id: int, attendance_update: AttendanceSchema) -> dict:
        return self.attendance_service.update_attendance(attendance_id, attendance_update)

    def delete_attendance(self, attendance_id: int) -> dict:
        return self.attendance_service.delete_attendance(attendance_id)

    def get_sla_metrics(self) -> dict:
        return self.attendance_service.get_sla_metrics()

    def get_sla_metrics_by_green_angels(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        return self.attendance_service.get_sla_paginated_by_green_angels(page, per_page, filters, order_by, order_direction)

    def get_sla_by_green_angel(self, green_angel_id: int) -> dict:
        return self.attendance_service.find_sla_by_green_angel(green_angel_id)

    def get_sla_metrics_by_hubs(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        return self.attendance_service.get_sla_paginated_by_hubs(page, per_page, filters, order_by, order_direction)

    def get_sla_by_hub(self, hub_id: int) -> dict:
        return self.attendance_service.find_sla_by_hub(hub_id)

    def get_productivity_metrics(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        return self.attendance_service.get_productivity_paginated(page, per_page, filters, order_by, order_direction)
