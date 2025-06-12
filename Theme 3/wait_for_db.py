import os
import time
import psycopg2
from psycopg2 import OperationalError

print("Waiting PostgreSQL...")

while True:
    try:
        conn = psycopg2.connect(
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ["POSTGRES_HOST"],
            port=os.environ.get("POSTGRES_PORT", 5432),
        )
        conn.close()
        print("✅ PostgreSQL is available!")
        break
    except OperationalError:
        print("❌ Database unavailable, retrying in 1 second...")
        time.sleep(1)
