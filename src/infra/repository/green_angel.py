from typing import Type
from sqlalchemy.orm import Session

from src.domain.entities.green_angel import GreenAngel
from src.domain.repository.green_angel import IGreenAngelRepository


class GreenAngelRepository(IGreenAngelRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_green_angels_paginated(self, page: int, per_page: int, filters: dict = None, order_by: str = 'id', order_direction: str = 'asc') -> dict:
        total = self.db.query(GreenAngel).count()
        query = self.db.query(GreenAngel).filter(GreenAngel.is_active == True)

        if filters:
            if 'name' in filters and filters['name']:
                query = query.filter(GreenAngel.name.ilike(f"%{filters['name']}%"))

        allowed_order_by = ['id', 'name', 'is_active', 'created_at', 'updated_at']
        if order_by not in allowed_order_by:
            order_by = 'id'

        if order_direction == 'desc':
            query = query.order_by(getattr(GreenAngel, order_by).desc())
        else:
            query = query.order_by(getattr(GreenAngel, order_by))

        page = page if page > 0 else 1
        green_angels = query.offset((page - 1) * per_page).limit(per_page).all()
        return {
            'size': len(green_angels),
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'items': green_angels
        }

    def find_by_id(self, green_angel_id: int) -> Type[GreenAngel]:
        return self.db.query(GreenAngel).filter(GreenAngel.id == green_angel_id).first()

    def save(self, green_angel: GreenAngel) -> GreenAngel:
        self.db.add(green_angel)
        self.db.commit()
        self.db.refresh(green_angel)
        return green_angel

    def delete(self, green_angel: GreenAngel) -> GreenAngel:
        self.db.delete(green_angel)
        self.db.commit()
        return green_angel
