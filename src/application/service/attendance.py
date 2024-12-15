from src.domain.exception.domain_exception import DomainException
from src.domain.exception.error_code import ErrorCode
from src.domain.repository.attendance import IAttendanceRepository
from src.domain.repository.client import IClientRepository
from src.domain.repository.green_angel import IGreenAngelRepository
from src.domain.repository.hub import IHubRepository
from src.domain.entities.attendance import Attendance
from src.interface.web.schemas.attendance import (
    AttendanceSchema, AttendancesPaginatedSchema, AttendanceUpdateSchema)


class AttendanceService:
    def __init__(self, attendance_repository: IAttendanceRepository, green_angel_repository: IGreenAngelRepository, hub_repository: IHubRepository, client_repository: IClientRepository):
        self.attendance_repository = attendance_repository
        self.green_angel_repository = green_angel_repository
        self.hub_repository = hub_repository
        self.client_repository = client_repository

    def get_attendances_paginated(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        attendances = self.attendance_repository.get_attendances_paginated(page, per_page, filters, order_by, order_direction)
        return AttendancesPaginatedSchema.model_validate(attendances).model_dump()

    def find_attendance(self, attendance_id: int) -> dict:
        attendance = self.attendance_repository.find_by_id(attendance_id)
        if not attendance:
            raise DomainException(ErrorCode.ATTENDANCE_NOT_FOUND)
        return AttendanceSchema.model_validate(attendance).model_dump()

    def create_attendance(self, attendance_create: AttendanceSchema) -> dict:
        if not self.green_angel_repository.find_by_id(attendance_create.green_angel_id):
            raise DomainException(ErrorCode.GREEN_ANGEL_NOT_FOUND)
        if not self.hub_repository.find_by_id(attendance_create.hub_id):
            raise DomainException(ErrorCode.HUB_NOT_FOUND)
        if not self.client_repository.find_by_id(attendance_create.client_id):
            raise DomainException(ErrorCode.CLIENT_NOT_FOUND)

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

    def get_sla_metrics(self) -> dict:
        return self.attendance_repository.get_sla_metrics()

    def get_sla_paginated_by_green_angels(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        return self.attendance_repository.get_sla_paginated_by_green_angels(page, per_page, filters, order_by, order_direction)

    def find_sla_by_green_angel(self, green_angel_id: int) -> dict:
        return self.attendance_repository.find_sla_by_green_angel_id(green_angel_id)

    def get_sla_paginated_by_hubs(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        return self.attendance_repository.get_sla_paginated_by_hubs(page, per_page, filters, order_by, order_direction)

    def find_sla_by_hub(self, hub_id: int) -> dict:
        return self.attendance_repository.find_sla_by_hub_id(hub_id)

    def get_productivity_paginated(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        return self.attendance_repository.get_productivity_paginated(page, per_page, filters, order_by, order_direction)
