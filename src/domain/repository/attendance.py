from abc import ABC, abstractmethod

from src.domain.entities.attendance import Attendance


class IAttendanceRepository(ABC):

    @abstractmethod
    def get_attendances_paginated(self, page: int, per_page: int):
        pass

    @abstractmethod
    def find_by_id(self, attendance_id : int):
        pass

    @abstractmethod
    def save(self, attendance: Attendance):
        pass

    @abstractmethod
    def delete(self, attendance: Attendance):
        pass
