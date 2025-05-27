import sqlite3
from lib.db.connection import get_connection
from lib.db.seed import seed_data

def setup_database():
    conn = get_connection()
    with open('lib/db/schema.sql', 'r') as f:
        schema = f.read()
    
    try:
        cursor = conn.cursor()
        cursor.executescript(schema)
        seed_data(conn)
        print("Database setup complete.")
    except Exception as e:
        print(f"An error occurred while setting up the database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()