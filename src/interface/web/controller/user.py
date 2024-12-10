from typing import List

from src.interface.web.schemas.user import (UserCreateSchema, UserUpdateSchema)
from src.application.service.user import UserService


class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_users(self) -> List[dict]:
        return self.user_service.get_users_paginated()

    def get_user(self, user_id: int) -> dict:
        return self.user_service.find_user(user_id)

    def create_user(self, user_create: UserCreateSchema) -> dict:
        return self.user_service.create_user(user_create)

    def update_user(self, user_id: int, user_update: UserUpdateSchema) -> dict:
        return self.user_service.update_user(user_id, user_update)

    def delete_user(self, user_id: int) -> dict:
        return self.user_service.delete_user(user_id)
