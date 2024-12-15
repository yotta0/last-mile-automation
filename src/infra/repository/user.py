from typing import Type, List
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.domain.entities.user import User
from src.domain.repository.user import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_users_paginated(self, page: int, per_page: int, filters: dict = None, order_by: str = 'id', order_direction: str = 'asc') -> dict:
        total = self.db.query(User).count()

        query = self.db.query(User).filter(User.is_active == True)

        if filters:
            if 'name' in filters and filters['name']:
                query = query.filter(User.name.ilike(f"%{filters['name']}%"))
            if 'email' in filters and filters['email']:
                query = query.filter(User.email == filters['email'])

        allowed_order_by = ['id', 'name', 'email', 'is_active', 'created_at', 'updated_at']
        if order_by not in allowed_order_by:
            order_by = 'id'

        if order_direction == 'desc':
            query = query.order_by(getattr(User, order_by).desc())
        else:
            query = query.order_by(getattr(User, order_by))

        page = page if page > 0 else 1
        users = query.offset((page - 1) * per_page).limit(per_page).all()
        return {
            'size': len(users),
            'total_pages': (total + per_page - 1) // per_page,
            'page': page,
            'per_page': per_page,
            'items': users
        }

    def find_by_id(self, user_id: int) -> Type[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def find_by_email(self, email: EmailStr) -> Type[User]:
        return self.db.query(User).filter(User.email == email).first()

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> User:
        self.db.delete(user)
        self.db.commit()
        return user
