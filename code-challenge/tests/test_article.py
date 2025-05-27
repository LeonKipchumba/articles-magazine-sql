import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.seed import seed, create_schema

@pytest.fixture(autouse=True)
def seed_db():
    from lib.db.seed import delete_db
    delete_db()
    create_schema()
    seed()
    yield

# Test Article creation and validation
def test_article_creation(seed_db):
    author = Author.find_by_name("Alice Smith")
    magazine = Magazine.find_by_id(1)
    assert author is not None
    assert magazine is not None
    article = Article("Test Article", author, magazine)
    article.save()
    found = Article.find_by_id(article.id)
    assert found is not None
    assert found.title == "Test Article"
    assert found.author.id == author.id
    assert found.magazine.id == magazine.id
    with pytest.raises(ValueError):
        Article("   ", author, magazine)

def test_find_by_id(seed_db):
    author = Author.find_by_name("Alice Smith")
    magazine = Magazine.find_by_id(1)
    assert author is not None
    assert magazine is not None
    article = Article("Unique Article", author, magazine)
    article.save()
    found = Article.find_by_id(article.id)
    assert found is not None
    assert found.title == "Unique Article"

def test_find_articles_by_author(seed_db):
    author = Author.find_by_name("Alice Smith")
    magazine1 = Magazine.find_by_id(1)
    magazine2 = Magazine.find_by_id(2)
    assert author is not None
    assert magazine1 is not None
    assert magazine2 is not None
    article1 = Article("Article by Alice in Magazine 1", author, magazine1)
    article1.save()
    article2 = Article("Article by Alice in Magazine 2", author, magazine2)
    article2.save()
    articles = [a for a in author.articles() if a.title in ["Article by Alice in Magazine 1", "Article by Alice in Magazine 2"]]
    assert len(articles) == 2
    titles = [a.title for a in articles]
    assert "Article by Alice in Magazine 1" in titles
    assert "Article by Alice in Magazine 2" in titles

def test_find_articles_by_magazine(seed_db):
    author1 = Author.find_by_name("Alice Smith")
    author2 = Author.find_by_name("Bob Brown")
    if not author2:
        author2 = Author("Bob Brown")
        author2.save()
    magazine = Magazine.find_by_id(1)
    assert author1 is not None
    assert author2 is not None
    assert magazine is not None
    article1 = Article("Article in Magazine 1 by Alice", author1, magazine)
    article1.save()
    article2 = Article("Article in Magazine 1 by Bob", author2, magazine)
    article2.save()
    articles = [a for a in magazine.articles() if a.title in ["Article in Magazine 1 by Alice", "Article in Magazine 1 by Bob"]]
    assert len(articles) == 2
    titles = [a.title for a in articles]
    assert "Article in Magazine 1 by Alice" in titles
    assert "Article in Magazine 1 by Bob" in titles

def test_article_relationships(seed_db):
    author = Author.find_by_name("Alice Smith")
    magazine = Magazine.find_by_id(1)
    assert author is not None
    assert magazine is not None
    article = Article("Article with Relationships", author, magazine)
    article.save()
    assert article.author.id == author.id
    assert article.magazine.id == magazine.id

def test_article_title_validation(seed_db):
    author = Author.find_by_name("Alice Smith")
    magazine = Magazine.find_by_id(1)
    assert author is not None
    assert magazine is not None
    with pytest.raises(ValueError):
        Article(title="", author=author, magazine=magazine)