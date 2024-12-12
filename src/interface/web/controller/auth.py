from src.interface.web.schemas.user import (UserAuthSchema)
from src.application.service.auth import AuthService


class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def login(self, user_auth: UserAuthSchema) -> dict:
        return self.auth_service.verify_password(user_auth)
