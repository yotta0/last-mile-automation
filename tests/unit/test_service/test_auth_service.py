import uuid
import pytest
from unittest.mock import MagicMock, patch

from passlib.context import CryptContext
from src.application.service.auth import AuthService
from src.domain.entities.user import User
from src.interface.web.middleware.jwt_handler import JWTHandler
from src.interface.web.schemas.user import (UserAuthSchema)
from src.domain.exception.domain_exception import DomainException
from src.domain.exception.error_code import ErrorCode
from src.infra.config.config import get_settings


class TestAuthService:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_repository_mock = MagicMock()
        self.auth_service = AuthService(user_repository=self.user_repository_mock)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.settings = get_settings()

        self.default_user = User(
            id=1,
            name="test_user",
            email="test@email.com"
        )

    def test_get_password_hash(self):
        """Test if the password hash is generated correctly."""
        password = self.settings.SECRET_KEY
        hashed_password = self.auth_service.get_password_hash(password)
        assert self.pwd_context.verify(password, hashed_password)

    def test_verify_password_user_not_found(self):
        """Test if the correct exception is raised when the user is not found."""
        user_auth = UserAuthSchema(email="testuser@email.com", password="password")
        self.user_repository_mock.find_by_email.return_value = None

        with pytest.raises(DomainException) as excinfo:
            self.auth_service.verify_password(user_auth)

        assert excinfo.value.error_code == ErrorCode.UNAUTHORIZED

    def test_verify_password_invalid_password(self):
        """Test if the correct exception is raised when the password is incorrect."""
        user_auth = UserAuthSchema(email="test_user@username.com", password="password123")
        mock_user = User(
            name="test_user",
            email="test_user@username.com",
            hashed_password=self.auth_service.get_password_hash("password")
        )
        self.user_repository_mock.find_by_email.return_value = mock_user

        with pytest.raises(DomainException) as excinfo:
            self.auth_service.verify_password(user_auth)

        assert excinfo.value.error_code == ErrorCode.UNAUTHORIZED

    @patch.object(JWTHandler, 'create_refresh_token', return_value="mocked_token")
    def test_verify_password_success(self, mock_create_refresh_token):
        """Test if a token is generated when the username and password are correct."""
        user_auth = UserAuthSchema(email="test_user@username.com", password="password123")
        mock_user = User(
            name="test_user",
            email="test_user@username.com",
            hashed_password=self.auth_service.get_password_hash("password123"),
            id=1
        )
        self.user_repository_mock.find_by_email.return_value = mock_user

        token = self.auth_service.verify_password(user_auth)

        assert token['refresh_token'] == "mocked_token"
        mock_create_refresh_token.assert_called_once_with({
            "sub": mock_user.email,
            "id": str(mock_user.id)
        })

    def test_verify_old_password_success(self):
        """Test if the old password is verified correctly."""
        old_password = "old_password"
        password = self.auth_service.get_password_hash(old_password)
        assert self.auth_service.verify_old_password(old_password, password)

    def test_verify_old_password_invalid(self):
        """Test if the old password is invalid."""
        old_password = "old_password"
        password = self.auth_service.get_password_hash("new_password")
        assert not self.auth_service.verify_old_password(old_password, password)
