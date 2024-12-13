from passlib.context import CryptContext
from datetime import datetime as dt

from src.domain.exception.domain_exception import DomainException
from src.domain.exception.error_code import ErrorCode
from src.domain.repository.user import IUserRepository
from src.interface.web.schemas.token import TokenSchema, AccessTokenSchema
from src.interface.web.schemas.user import UserAuthSchema
from src.interface.web.middleware.jwt_handler import JWTHandler


class AuthService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, user_auth: UserAuthSchema) -> dict:
        user = self.user_repository.find_by_email(user_auth.email)
        if not user or not self.pwd_context.verify(user_auth.password, user.hashed_password):
            raise DomainException(ErrorCode.UNAUTHORIZED)
        payload = {
            "sub": user.email,
            "id": str(user.id)
        }

        refresh_token = JWTHandler.create_refresh_token(payload)
        access_token = JWTHandler.create_access_token(payload)
        user.last_login = dt.utcnow()
        self.user_repository.save(user)
        return TokenSchema(refresh_token=refresh_token, access_token=access_token).model_dump()

    def verify_old_password(self, old_password, password) -> bool:
        return self.pwd_context.verify(old_password, password)

    def refresh_token(self, sub: str, id: int) -> dict:
        payload = {
            "sub": sub,
            "id": id
        }
        access_token = JWTHandler.create_access_token(payload)
        return AccessTokenSchema(access_token=access_token).model_dump()
