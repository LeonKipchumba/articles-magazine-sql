import sys
from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

def run_queries():
    conn = get_connection()
    
    try:
        cursor = conn.cursor()

        # Example query: Get all authors
        cursor.execute("SELECT * FROM authors")
        authors = cursor.fetchall()
        print("Authors:")
        for author in authors:
            print(author)

        # Example query: Get all magazines
        cursor.execute("SELECT * FROM magazines")
        magazines = cursor.fetchall()
        print("\nMagazines:")
        for magazine in magazines:
            print(magazine)

        # Example query: Get all articles
        cursor.execute("SELECT * FROM articles")
        articles = cursor.fetchall()
        print("\nArticles:")
        for article in articles:
            print(article)

        # Example query: Get articles by a specific author
        author_id = input("\nEnter author ID to find their articles: ")
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
        author_articles = cursor.fetchall()
        print(f"\nArticles by Author ID {author_id}:")
        for article in author_articles:
            print(article)

        # Example query: Get magazines that published articles by a specific author
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (author_id,))
        author_magazines = cursor.fetchall()
        print(f"\nMagazines that published articles by Author ID {author_id}:")
        for magazine in author_magazines:
            print(magazine)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_queries()