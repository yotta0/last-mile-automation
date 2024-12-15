from typing import Type
from sqlalchemy.orm import Session

from src.domain.entities.client import Client
from src.domain.repository.client import IClientRepository


class ClientRepository(IClientRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_clients_paginated(self, page: int, per_page: int, order_by: str = 'id', order_direction: str = 'asc') -> dict:
        total = self.db.query(Client).count()

        query = self.db.query(Client).filter(Client.is_active == True)

        allowed_order_by = ['id', 'is_active', 'created_at', 'updated_at']
        if order_by not in allowed_order_by:
            order_by = 'id'

        if order_direction == 'desc':
            query = query.order_by(getattr(Client, order_by).desc())
        else:
            query = query.order_by(getattr(Client, order_by))

        page = page if page > 0 else 1
        clients = query.offset((page - 1) * per_page).limit(per_page).all()
        return {
            'size': len(clients),
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'items': clients
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
