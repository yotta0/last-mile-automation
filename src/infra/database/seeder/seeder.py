import os
import pandas as pd
import psycopg2
from datetime import datetime as dt
from dotenv import load_dotenv
from psycopg2 import pool
from passlib.context import CryptContext

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
CSV_FILE_PATH = os.getenv('CSV_FILE_PATH', 'src/infra/database/seeder/seed.csv')

conn_pool = psycopg2.pool.SimpleConnectionPool(1, 10, SQLALCHEMY_DATABASE_URI)

def convert_date(date_str):
    if pd.isna(date_str) or date_str.strip() == '' or date_str.strip() == '-':
        return None
    try:
        dt.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return date_str
    except ValueError:
        try:
            return pd.to_datetime(date_str.strip(), format='%d/%m%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return pd.to_datetime(date_str.strip(), format='mixed', dayfirst=True).strftime('%Y-%m-%d %H:%M:%S')

def import_csv():
    df = pd.read_csv(CSV_FILE_PATH, delimiter=';')
    df = df.head(10000)

    df['data_limite'] = df['data_limite'].apply(convert_date)
    df['data_de_atendimento'] = df['data_de_atendimento'].apply(convert_date)

    green_angels_data = [(row['angel'], True, dt.utcnow(), dt.utcnow()) for index, row in df.iterrows()]
    hubs_data = [(row['polo'], True, dt.utcnow(), dt.utcnow()) for index, row in df.iterrows()]
    clients_data = [(row['id_cliente'], True, dt.utcnow(), dt.utcnow()) for index, row in df.iterrows()]
    attendances_data = [(row['id_atendimento'], row['id_cliente'], None, None, row['data_limite'], row['data_de_atendimento'], True, dt.utcnow(), dt.utcnow()) for index, row in df.iterrows()]

    conn = conn_pool.getconn()
    cur = conn.cursor()

    green_angel_ids = []
    for data in green_angels_data:
        cur.execute("INSERT INTO green_angels (name, is_active, created_at, updated_at) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING returning id", data)
        green_angel_ids.append(cur.fetchone()[0])

    hub_ids = []
    for data in hubs_data:
        cur.execute("INSERT INTO hubs (name, is_active, created_at, updated_at) VALUES (%s, %s, %s, %s) ON CONFLICT (name) DO UPDATE SET updated_at = NOW() returning id", data)
        hub_ids.append(cur.fetchone()[0])

    client_id = []
    for data in clients_data:
        cur.execute("INSERT INTO clients (id, is_active, created_at, updated_at) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET updated_at = NOW() returning id", data)
        client_id.append(cur.fetchone()[0])

    for i in range(len(attendances_data)):
        attendances_data[i] = (attendances_data[i][0], client_id[i], green_angel_ids[i], hub_ids[i], attendances_data[i][4], attendances_data[i][5], attendances_data[i][6], attendances_data[i][7], attendances_data[i][8])

    cur.executemany("INSERT INTO attendances (id, client_id, green_angel_id, hub_id, limit_date, attendance_date, is_active, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", attendances_data)

    conn.commit()
    cur.close()
    conn_pool.putconn(conn)

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
    print("Importing CSV data...")
    import_csv()
    print("CSV data imported successfully!")
    print("Seeding users...")
    seed_users()
    print("Users seeded successfully!")
