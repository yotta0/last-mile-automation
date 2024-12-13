from typing import Type
from sqlalchemy.orm import Session

from src.domain.entities.client import Client
from src.domain.repository.client import IClientRepository


class ClientRepository(IClientRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_clients_paginated(self, page: int, per_page: int) -> dict:
        total = self.db.query(Client).count()
        clients = self.db.query(Client).offset((page - 1) * per_page).limit(per_page).all()
        return {
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'clients': clients
        }

    def find_by_id(self, client_id: int) -> Type[Client]:
        return self.db.query(Client).filter(Client.id == client_id).first()

    def save(self, client: Client) -> Client:
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def delete(self, client: Client) -> Client:
        self.db.delete(client)
        self.db.commit()
        return client
