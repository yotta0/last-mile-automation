from src.domain.exception.domain_exception import DomainException
from src.domain.exception.error_code import ErrorCode
from src.domain.repository.green_angel import IGreenAngelRepository
from src.domain.entities.green_angel import GreenAngel
from src.interface.web.schemas.green_angel import (
    GreenAngelSchema, GreenAngelsPaginatedSchema, GreenAngelUpdateSchema)


class GreenAngelService:
    def __init__(self, green_angel_repository: IGreenAngelRepository):
        self.green_angel_repository = green_angel_repository

    def get_green_angels_paginated(self, page: int, per_page: int) -> dict:
        green_angels = self.green_angel_repository.get_green_angels_paginated(page, per_page)
        return GreenAngelsPaginatedSchema.model_validate(green_angels).model_dump()

    def find_green_angel(self, green_angel_id: int) -> dict:
        green_angel = self.green_angel_repository.find_by_id(green_angel_id)
        if not green_angel:
            raise DomainException(ErrorCode.GREEN_ANGEL_NOT_FOUND)
        return GreenAngelSchema.model_validate(green_angel).model_dump()

    def create_green_angel(self, green_angel_create: GreenAngelSchema) -> dict:
        green_angel = GreenAngel(
            name=green_angel_create.name,
            is_active=green_angel_create.is_active
        )
        self.green_angel_repository.save(green_angel)
        return GreenAngelSchema.model_validate(green_angel).model_dump()

    def update_green_angel(self, green_angel_id: int, green_angel_update: GreenAngelUpdateSchema) -> dict:
        green_angel = self.green_angel_repository.find_by_id(green_angel_id)
        if not green_angel:
            raise DomainException(ErrorCode.ATTENDANCE_NOT_FOUND)

        if green_angel_update.name:
            green_angel.name = green_angel_update.name
        if green_angel_update.is_active:
            green_angel.is_active = green_angel_update.is_active
        self.green_angel_repository.save(green_angel)
        return GreenAngelSchema.model_validate(green_angel).model_dump()

    def delete_green_angel(self, green_angel_id: int) -> dict:
        green_angel = self.green_angel_repository.find_by_id(green_angel_id)
        if not green_angel:
            raise DomainException(ErrorCode.ATTENDANCE_NOT_FOUND)
        if not green_angel.is_active:
            raise DomainException(ErrorCode.ATTENDANCE_ALREADY_DELETED)
        green_angel.is_active = False
        self.green_angel_repository.save(green_angel)
        return GreenAngelSchema.model_validate(green_angel).model_dump()
