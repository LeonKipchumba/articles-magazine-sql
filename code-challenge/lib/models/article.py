# Article model for code-challenge
from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author, magazine, id=None):
        if author is None or magazine is None:
            raise ValueError("Article must have a valid author and magazine.")
        self._id = id
        self.title = title
        self.author = author
        self.magazine = magazine

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string.")
        self._title = value.strip()

    def save(self):
        if self.author is None or self.magazine is None:
            raise ValueError("Article must have a valid author and magazine before saving.")
        conn = get_connection()
        try:
            conn.execute("BEGIN TRANSACTION")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?) RETURNING id",
                (self.title, self.author.id, self.magazine.id)
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
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            from lib.models.author import Author
            from lib.models.magazine import Magazine
            author = Author.find_by_id(row["author_id"])
            magazine = Magazine.find_by_id(row["magazine_id"])
            return cls(row["title"], author, magazine, id=row["id"])
        return None
