from abc import ABC, abstractmethod

from src.domain.entities.attendance import Attendance


class IAttendanceRepository(ABC):

    @abstractmethod
    def get_attendances_paginated(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        pass

    @abstractmethod
    def find_by_id(self, attendance_id : int) -> Attendance:
        pass

    @abstractmethod
    def save(self, attendance: Attendance):
        pass

    @abstractmethod
    def delete(self, attendance: Attendance):
        pass

    @abstractmethod
    def get_sla_metrics(self) -> dict:
        pass

    def get_sla_paginated_by_green_angels(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        pass

    def find_sla_by_green_angel_id(self, green_angel_id: int) -> dict:
        pass

    def get_sla_paginated_by_hubs(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        pass

    def find_sla_by_hub_id(self, hub_id: int) -> dict:
        pass

    def get_productivity_paginated(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        pass
