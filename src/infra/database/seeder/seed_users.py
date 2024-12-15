import os
import psycopg2
from datetime import datetime as dt
from dotenv import load_dotenv
from psycopg2 import pool
from passlib.context import CryptContext

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

conn_pool = psycopg2.pool.SimpleConnectionPool(1, 10, SQLALCHEMY_DATABASE_URI)

def seed_users():
    conn = conn_pool.getconn()
    cur = conn.cursor()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("admin")

    cur.execute("INSERT INTO users (name, email, hashed_password, is_active, created_at, updated_at, last_login) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", ('admin', 'admin@admin.com', hashed_password, True, dt.utcnow(), dt.utcnow(), None))

    conn.commit()
    cur.close()
    conn_pool.putconn(conn)

if __name__ == "__main__":
    print("Seeding users...")
    seed_users()
    print("Users seeded successfully!")
