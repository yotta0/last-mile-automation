from src.interface.web.schemas.client import ClientCreateSchema, ClientUpdateSchema
from src.application.service.client import ClientService


class ClientController:
    def __init__(self, client_service: ClientService):
        self.client_service = client_service

    def get_clients(self, page: int, per_page: int, order_by: str, order_direction: str) -> dict:
        return self.client_service.get_clients_paginated(page, per_page, order_by, order_direction)

    def get_client(self, client_id: int) -> dict:
        return self.client_service.find_client(client_id)

    def create_client(self, client_create: ClientCreateSchema) -> dict:
        return self.client_service.create_client(client_create)

    def update_client(self, client_id: int, client_update: ClientUpdateSchema) -> dict:
        return self.client_service.update_client(client_id, client_update)

    def delete_client(self, client_id: int) -> dict:
        return self.client_service.delete_client(client_id)
