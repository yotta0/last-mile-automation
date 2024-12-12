from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

from src.domain.entities.user import User
from src.infra.database.database import SessionLocal


def seed_data():
    session = SessionLocal()

    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password = pwd_context.hash("admin")
        user = User(id="38ef5013-cf60-4e3b-8553-e9a78cabce05", name="admin", email="admin@admin.com", hashed_password=password)
        session.add_all([user])
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Erro ao executar o seeder: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    try:
        seed_data()
    except Exception:
        pass
