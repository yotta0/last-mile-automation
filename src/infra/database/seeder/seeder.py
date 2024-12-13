import os
import pandas as pd
import threading
import psycopg2
from datetime import datetime as dt
from dotenv import load_dotenv
from psycopg2 import pool
from passlib.context import CryptContext
import time

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
    if not os.path.isfile(CSV_FILE_PATH):
        print("CSV file not found!")
        return

    batch_size = 1000
    df_iter = pd.read_csv(CSV_FILE_PATH, delimiter=';', chunksize=batch_size)
    batch_num = 0

    for batch_df in df_iter:
        start_time = time.time()

        batch_df['data_limite'] = batch_df['data_limite'].apply(convert_date)
        batch_df['data_de_atendimento'] = batch_df['data_de_atendimento'].apply(convert_date)

        green_angels_data = [(row['angel'], True, dt.utcnow(), dt.utcnow()) for index, row in batch_df.iterrows()]
        hubs_data = [(row['polo'], True, dt.utcnow(), dt.utcnow()) for index, row in batch_df.iterrows()]
        clients_data = [(row['id_cliente'], True, dt.utcnow(), dt.utcnow()) for index, row in batch_df.iterrows()]

        conn = conn_pool.getconn()
        cur = conn.cursor()

        try:
            # Process the batch in the database
            green_angel_ids = {}
            for data in green_angels_data:
                cur.execute(
                    "INSERT INTO green_angels (name, is_active, created_at, updated_at) VALUES (%s, %s, %s, %s) ON CONFLICT (name) DO UPDATE SET updated_at = NOW() RETURNING id, name",
                    data)
                result = cur.fetchone()
                green_angel_ids[result[1]] = result[0]

            hub_ids = {}
            for data in hubs_data:
                cur.execute(
                    "INSERT INTO hubs (name, is_active, created_at, updated_at) VALUES (%s, %s, %s, %s) ON CONFLICT (name) DO UPDATE SET updated_at = NOW() RETURNING id, name",
                    data)
                result = cur.fetchone()
                hub_ids[result[1]] = result[0]

            client_ids = {}
            for data in clients_data:
                cur.execute(
                    "INSERT INTO clients (id, is_active, created_at, updated_at) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET updated_at = NOW() RETURNING id",
                    data)
                result = cur.fetchone()
                client_ids[result[0]] = result[0]

            attendances_data = [(row['id_atendimento'], client_ids.get(row['id_cliente']), green_angel_ids.get(row['angel']),
                                 hub_ids.get(row['polo']), row['data_limite'],
                                 row['data_de_atendimento'], True, dt.utcnow(), dt.utcnow()) for index, row in batch_df.iterrows()]

            # Filter out rows with null green_angel_id, hub_id, or client_id
            attendances_data = [data for data in attendances_data if data[1] is not None and data[2] is not None and data[3] is not None]

            cur.executemany(
                "INSERT INTO attendances (id, client_id, green_angel_id, hub_id, limit_date, attendance_date, is_active, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                attendances_data)

            conn.commit()
        except Exception as e:
            print(f"Error processing batch {batch_num}: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn_pool.putconn(conn)

        # Evaluate the processing time of the batch
        elapsed_time = time.time() - start_time
        print(f"Processed batch {batch_num} with {len(batch_df)} rows in {elapsed_time:.2f} seconds.")

        # Dynamically adjust the batch size (optional)
        if elapsed_time < 1:
            batch_size = min(batch_size + 1000, 10000)  # Gradually increase the batch size
        elif elapsed_time > 5:
            batch_size = max(batch_size - 500, 500)  # Reduce the batch size if too slow

        batch_num += 1

def seed_users():
    conn = conn_pool.getconn()
    cur = conn.cursor()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("admin")

    cur.execute("INSERT INTO users (name, email, hashed_password, is_active, created_at, updated_at, last_login) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", ('admin', 'admin@admin.com', hashed_password, True, dt.utcnow(), dt.utcnow(), None))

    conn.commit()
    cur.close()
    conn_pool.putconn(conn)

def run_import_csv_in_background():
    thread = threading.Thread(target=import_csv)
    thread.start()
    return thread

if __name__ == "__main__":
    print("Seeding users...")
    seed_users()
    print("Users seeded successfully!")
    print("Importing CSV data in batches...")
    run_import_csv_in_background()
    print("CSV data imported successfully!")
