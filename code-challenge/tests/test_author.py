import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed, create_schema

@pytest.fixture(autouse=True)
def seed_db():
    from lib.db.seed import delete_db
    delete_db()
    create_schema()
    seed()
    yield

# Test Author creation and validation
def test_create_author(seed_db):
    author = Author(name="Test Author")
    author.save()
    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.name == "Test Author"

    with pytest.raises(ValueError):
        Author(name="   ")

# Test find_by_name
def test_find_by_name(seed_db):
    author = Author.find_by_name("Alice Smith")
    assert author is not None
    assert author.name == "Alice Smith"

# Test articles() relationship
def test_author_articles(seed_db):
    author = Author.find_by_name("Alice Smith")
    articles = author.articles()
    assert isinstance(articles, list)
    assert all(isinstance(a, Article) for a in articles)
    assert any(a.title == "AI Revolution" for a in articles)

# Test magazines() relationship
def test_author_magazines(seed_db):
    author = Author.find_by_name("Alice Smith")
    magazines = author.magazines()
    assert isinstance(magazines, list)
    assert any(m.name == "Tech Today" for m in magazines)

# Test add_article
def test_add_article(seed_db):
    author = Author.find_by_name("Alice Smith")
    magazine = Magazine.find_by_id(1)
    article = author.add_article(magazine, "New Article")
    assert article.title == "New Article"
    assert article.author.id == author.id
    assert article.magazine.id == magazine.id

# Test topic_areas
def test_topic_areas(seed_db):
    author = Author.find_by_name("Alice Smith")
    topics = author.topic_areas()
    assert "Technology" in topics
    assert isinstance(topics, list)