import re

from src.application.service.auth import AuthService
from src.domain.exception.domain_exception import DomainException
from src.domain.exception.error_code import ErrorCode
from src.domain.repository.user import IUserRepository
from src.domain.entities.user import User
from src.interface.web.schemas.user import (
    UserCreateSchema, UserSchema, UserUpdateSchema, UsersPaginatedSchema)



class UserService:
    def __init__(self, user_repository: IUserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service
        self.rule_password = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$'

    def get_users_paginated(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        users = self.user_repository.get_users_paginated(page, per_page, filters, order_by, order_direction)
        return UsersPaginatedSchema.model_validate(users).model_dump()

    def find_user(self, user_id: int) -> dict:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise DomainException(ErrorCode.USER_NOT_FOUND)
        return UserSchema.model_validate(user).model_dump()

    def create_user(self, user_create: UserCreateSchema) -> dict:
        if not re.match(self.rule_password, user_create.hashed_password):
            raise DomainException(ErrorCode.BAD_FORMAT_PASSWORD)

        if self.user_repository.find_by_email(user_create.email):
            raise DomainException(ErrorCode.USER_EXIST)

        hash_password = self.auth_service.get_password_hash(user_create.hashed_password)
        user = User(
            name=user_create.name,
            email=user_create.email,
            hashed_password=hash_password
        )
        self.user_repository.save(user)
        return UserSchema.model_validate(user).model_dump()

    def update_user(self, user_id: int, user_update: UserUpdateSchema) -> dict:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise DomainException(ErrorCode.USER_NOT_FOUND)
        if user_update.name:
            user.name = user_update.name
        if user_update.email:
            user.email = user_update.email
        if user_update.is_active:
            user.is_active = user_update.is_active
        self.user_repository.save(user)
        return UserSchema.model_validate(user).model_dump()

    def delete_user(self, user_id: int) -> dict:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise DomainException(ErrorCode.USER_NOT_FOUND)
        self.user_repository.delete(user)
        return UserSchema.model_validate(user).model_dump()
