# Magazine model for code-challenge
from lib.db.connection import get_connection
from lib.models.article import Article

class Magazine:
    def __init__(self, name, category, id=None):
        self._id = id
        self.name = name
        self.category = category

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

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Category must be a non-empty string.")
        self._category = value.strip()

    def save(self):
        conn = get_connection()
        try:
            conn.execute("BEGIN TRANSACTION")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?) RETURNING id",
                (self.name, self.category)
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
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["name"], row["category"], id=row["id"])
        return None

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        articles = cursor.fetchall()
        conn.close()
        from lib.models.author import Author
        return [Article(row["title"], Author.find_by_id(row["author_id"]), self, id=row["id"]) for row in articles]

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT a.* FROM authors a JOIN articles ar ON a.id = ar.author_id WHERE ar.magazine_id = ?", (self.id,))
        authors = cursor.fetchall()
        conn.close()
        from lib.models.author import Author
        return [Author(row["name"], id=row["id"]) for row in authors]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        titles = [row["title"] for row in cursor.fetchall()]
        conn.close()
        return titles

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT a.*, COUNT(ar.id) as article_count FROM authors a JOIN articles ar ON a.id = ar.author_id WHERE ar.magazine_id = ? GROUP BY a.id HAVING article_count > 2", (self.id,))
        authors = cursor.fetchall()
        conn.close()
        from lib.models.author import Author
        return [Author(row["name"], id=row["id"]) for row in authors]

    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT m.*, COUNT(a.id) as article_count FROM magazines m LEFT JOIN articles a ON m.id = a.magazine_id GROUP BY m.id ORDER BY article_count DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["name"], row["category"], id=row["id"])
        return None
