from typing import Type
from sqlalchemy.orm import Session

from src.domain.entities.hub import Hub
from src.domain.repository.hub import IHubRepository


class HubRepository(IHubRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_hubs_paginated(self, page: int, per_page: int, filters: dict = None, order_by: str = 'id', order_direction: str = 'asc') -> dict:
        total = self.db.query(Hub).count()
        query = self.db.query(Hub).filter(Hub.is_active == True)

        if filters:
            if 'name' in filters and filters['name']:
                query = query.filter(Hub.name.ilike(f"%{filters['name']}%"))

        allowed_order_by = ['id', 'name', 'is_active', 'created_at', 'updated_at']
        if order_by not in allowed_order_by:
            order_by = 'id'

        if order_direction == 'desc':
            query = query.order_by(getattr(Hub, order_by).desc())
        else:
            query = query.order_by(getattr(Hub, order_by))

        page = page if page > 0 else 1
        hubs = query.offset((page - 1) * per_page).limit(per_page).all()
        return {
            'size': len(hubs),
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'items': hubs
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
