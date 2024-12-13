import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from passlib.context import CryptContext
from sqlalchemy.orm import declarative_base

from src.main import app
from src.infra.database.database import get_db
from src.infra.config.config import get_settings

from src.interface.web.schemas.user import UserSchema
from src.domain.entities.user import User

settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password = pwd_context.hash("admin")
    user = User(name="admin", hashed_password=password, email="admin123@user.com")
    session.add_all([user])
    session.commit()

    yield session
    session.close()
    transaction.rollback()
    connection.close()
