from typing import Type
from sqlalchemy.orm import Session

from src.domain.entities.hub import Hub
from src.domain.repository.hub import IHubRepository


class HubRepository(IHubRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_hubs_paginated(self, page: int, per_page: int) -> dict:
        total = self.db.query(Hub).count()
        hubs = self.db.query(Hub).offset((page - 1) * per_page).limit(per_page).all()
        return {
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'hubs': hubs
        }

    def find_by_id(self, hub_id: int) -> Type[Hub]:
        return self.db.query(Hub).filter(Hub.id == hub_id).first()

    def save(self, hub: Hub) -> Hub:
        self.db.add(hub)
        self.db.commit()
        self.db.refresh(hub)
        return hub

    def delete(self, hub: Hub) -> Hub:
        self.db.delete(hub)
        self.db.commit()
        return hub
