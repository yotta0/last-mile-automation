from typing import Type
from sqlalchemy.orm import Session

from src.domain.entities.green_angel import GreenAngel
from src.domain.repository.green_angel import IGreenAngelRepository


class GreenAngelRepository(IGreenAngelRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_green_angels_paginated(self, page: int, per_page: int) -> dict:
        total = self.db.query(GreenAngel).count()
        green_angels = self.db.query(GreenAngel).offset((page - 1) * per_page).limit(per_page).all()
        return {
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'green_angels': green_angels
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
