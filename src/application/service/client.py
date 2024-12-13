from src.domain.exception.domain_exception import DomainException
from src.domain.exception.error_code import ErrorCode
from src.domain.repository.client import IClientRepository
from src.domain.entities.attendance import Client
from src.interface.web.schemas.client import (
    ClientSchema, ClientsPaginatedSchema, ClientUpdateSchema)


class ClientService:
    def __init__(self, client_repository: IClientRepository):
        self.client_repository = client_repository

    def get_clients_paginated(self, page: int, per_page: int) -> dict:
        clients = self.client_repository.get_clients_paginated(page, per_page)
        return ClientsPaginatedSchema.model_validate(clients).model_dump()

    def find_client(self, client_id: int) -> dict:
        client = self.client_repository.find_by_id(client_id)
        if not client:
            raise DomainException(ErrorCode.GREEN_ANGEL_NOT_FOUND)
        return ClientSchema.model_validate(client).model_dump()

    def create_client(self, client_create: ClientSchema) -> dict:
        client = Client(
            id=client_create.id,
            is_active=client_create.is_active
        )
        self.client_repository.save(client)
        return ClientSchema.model_validate(client).model_dump()

    def update_client(self, client_id: int, client_update: ClientUpdateSchema) -> dict:
        client = self.client_repository.find_by_id(client_id)
        if not client:
            raise DomainException(ErrorCode.ATTENDANCE_NOT_FOUND)

        if client_update.is_active:
            client.is_active = client_update.is_active
        self.client_repository.save(client)
        return ClientSchema.model_validate(client).model_dump()

    def delete_client(self, client_id: int) -> dict:
        client = self.client_repository.find_by_id(client_id)
        if not client:
            raise DomainException(ErrorCode.ATTENDANCE_NOT_FOUND)
        if not client.is_active:
            raise DomainException(ErrorCode.ATTENDANCE_ALREADY_DELETED)
        client.is_active = False
        self.client_repository.save(client)
        return ClientSchema.model_validate(client).model_dump()
