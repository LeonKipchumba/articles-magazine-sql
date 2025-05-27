import os
import sqlite3
from lib.db.connection import get_connection

SCHEMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'schema.sql')
DB_PATH = os.path.join(os.path.dirname(__file__), 'articles.db')

def create_schema():
    conn = get_connection()
    with open(SCHEMA_PATH, 'r') as f:
        schema = f.read()
    conn.executescript(schema)
    conn.close()

def delete_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def seed():
    conn = get_connection()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        # Clear existing data
        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM magazines")
        # Insert authors
        cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Alice Smith",))
        cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Bob Jones",))
        # Insert magazines
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Today", "Technology"))
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Health Weekly", "Health"))
        # Insert articles
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("AI Revolution", 1, 1))
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("Wellness Tips", 2, 2))
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("Tech & Health", 1, 2))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to seed database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    delete_db()
    create_schema()
    seed()
    print("Database schema created and seeded.")
