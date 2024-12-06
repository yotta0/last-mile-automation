from datetime import datetime, timedelta
import jwt
from flask import current_app

from src.interface.exception.error_code import ErrorCode
from src.interface.exception.interface_exception import InterfaceException
from src.infra.config.config import get_settings

settings = get_settings()

class JWTHandler:
    @staticmethod
    def create_refresh_token(payload: dict) -> str:
        to_encode = payload.copy()
        expire = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_access_token(payload: dict) -> str:
        to_encode = payload.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload if "sub" in payload else None
        except jwt.ExpiredSignatureError:
            raise InterfaceException(ErrorCode.EXPIRED_TOKEN)
        except jwt.InvalidTokenError:
            raise InterfaceException(ErrorCode.INVALID_TOKEN)