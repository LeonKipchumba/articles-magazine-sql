# Author model for code-challenge
from lib.db.connection import get_connection
from lib.models.article import Article

class Author:
    def __init__(self, name, id=None):
        self._id = id
        self.name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = value.strip()

    def save(self):
        conn = get_connection()
        try:
            conn.execute("BEGIN TRANSACTION")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO authors (name) VALUES (?) RETURNING id",
                (self.name,)
            )
            self._id = cursor.fetchone()[0]
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Failed to save: {e}")
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["name"], id=row["id"])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["name"], id=row["id"])
        return None

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        from lib.models.magazine import Magazine
        return [Article(row["title"], self, Magazine.find_by_id(row["magazine_id"]), id=row["id"]) for row in articles]

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT m.* FROM magazines m JOIN articles a ON m.id = a.magazine_id WHERE a.author_id = ?", (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        from lib.models.magazine import Magazine
        return [Magazine(row["name"], row["category"], id=row["id"]) for row in magazines]

    def add_article(self, magazine, title):
        article = Article(title, self, magazine)
        article.save()
        return article

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT m.category FROM magazines m JOIN articles a ON m.id = a.magazine_id WHERE a.author_id = ?", (self.id,))
        categories = [row["category"] for row in cursor.fetchall()]
        conn.close()
        return categories
