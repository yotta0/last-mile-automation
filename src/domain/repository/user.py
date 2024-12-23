from abc import ABC, abstractmethod
from pydantic import EmailStr

from src. domain.entities.user import User



class IUserRepository(ABC):

    @abstractmethod
    def get_users_paginated(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        pass

    @abstractmethod
    def find_by_id(self, user_id : int):
        pass

    @abstractmethod
    def find_by_email(self, email: EmailStr):
        pass

    @abstractmethod
    def save(self, user: User):
        pass

    @abstractmethod
    def delete(self, user: User):
        pass
