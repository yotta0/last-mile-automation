from src.interface.web.schemas.hub import HubCreateSchema, HubUpdateSchema
from src.application.service.hub import HubService


class HubController:
    def __init__(self, hub_service: HubService):
        self.hub_service = hub_service

    def get_hubs(self, page: int, per_page: int) -> dict:
        return self.hub_service.get_hubs_paginated(page, per_page)

    def get_hub(self, hub_id: int) -> dict:
        return self.hub_service.find_hub(hub_id)

    def create_hub(self, hub_create: HubCreateSchema) -> dict:
        return self.hub_service.create_hub(hub_create)

    def update_hub(self, hub_id: int, hub_update: HubUpdateSchema) -> dict:
        return self.hub_service.update_hub(hub_id, hub_update)

    def delete_hub(self, hub_id: int) -> dict:
        return self.hub_service.delete_hub(hub_id)
