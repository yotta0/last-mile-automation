import os
from functools import lru_cache

from dotenv import load_dotenv

class Settings:
    def __init__(self):
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.ALGORITHM = os.getenv('ALGORITHM')
        self.ACCESS_TOKEN_EXPIRE = int(os.getenv('ACCESS_TOKEN_EXPIRE', 8))

        self.SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


@lru_cache
def get_settings():
    load_dotenv()
    return Settings()
