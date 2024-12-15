from src.domain.exception.domain_exception import DomainException
from src.domain.exception.error_code import ErrorCode
from src.domain.repository.hub import IHubRepository
from src.domain.entities.attendance import Hub
from src.interface.web.schemas.hub import (
    HubSchema, HubsPaginatedSchema, HubUpdateSchema)


class HubService:
    def __init__(self, hub_repository: IHubRepository):
        self.hub_repository = hub_repository

    def get_hubs_paginated(self, page: int, per_page: int, filters: dict, order_by: str, order_direction: str) -> dict:
        hubs = self.hub_repository.get_hubs_paginated(page, per_page, filters, order_by, order_direction)
        return HubsPaginatedSchema.model_validate(hubs).model_dump()

    def find_hub(self, hub_id: int) -> dict:
        hub = self.hub_repository.find_by_id(hub_id)
        if not hub:
            raise DomainException(ErrorCode.HUB_NOT_FOUND)
        return HubSchema.model_validate(hub).model_dump()

    def create_hub(self, hub_create: HubSchema) -> dict:
        hub = Hub(
            name=hub_create.name,
            is_active=hub_create.is_active
        )
        self.hub_repository.save(hub)
        return HubSchema.model_validate(hub).model_dump()

    def update_hub(self, hub_id: int, hub_update: HubUpdateSchema) -> dict:
        hub = self.hub_repository.find_by_id(hub_id)
        if not hub:
            raise DomainException(ErrorCode.HUB_NOT_FOUND)

        if hub_update.name:
            hub.name = hub_update.name
        if hub_update.is_active:
            hub.is_active = hub_update.is_active
        self.hub_repository.save(hub)
        return HubSchema.model_validate(hub).model_dump()

    def delete_hub(self, hub_id: int) -> dict:
        hub = self.hub_repository.find_by_id(hub_id)
        if not hub:
            raise DomainException(ErrorCode.HUB_NOT_FOUND)
        if not hub.is_active:
            raise DomainException(ErrorCode.HUB_ALREADY_DELETED)
        hub.is_active = False
        self.hub_repository.save(hub)
        return HubSchema.model_validate(hub).model_dump()
