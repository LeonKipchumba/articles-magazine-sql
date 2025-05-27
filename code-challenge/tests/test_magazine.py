import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.seed import seed, create_schema

@pytest.fixture(autouse=True)
def seed_db():
    from lib.db.seed import delete_db
    delete_db()
    create_schema()
    seed()
    yield

def test_create_magazine(seed_db):
    magazine = Magazine(name="Test Mag", category="Science")
    magazine.save()
    found = Magazine.find_by_id(magazine.id)
    assert found is not None
    assert found.name == "Test Mag"
    assert found.category == "Science"

    with pytest.raises(ValueError):
        Magazine(name="", category="Science")
    with pytest.raises(ValueError):
        Magazine(name="Test", category=" ")

def test_articles(seed_db):
    magazine = Magazine.find_by_id(1)
    articles = magazine.articles()
    assert isinstance(articles, list)
    assert any(a.title == "AI Revolution" for a in articles)

def test_contributors(seed_db):
    magazine = Magazine.find_by_id(1)
    contributors = magazine.contributors()
    assert isinstance(contributors, list)
    assert any(a.name == "Alice Smith" for a in contributors)

def test_article_titles(seed_db):
    magazine = Magazine.find_by_id(1)
    titles = magazine.article_titles()
    assert "AI Revolution" in titles