from typing import Type, List
from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.domain.entities.user import User
from src.domain.repository.user import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_users_paginated(self) -> List[Type[User]]:
        return self.db.query(User).all()

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
