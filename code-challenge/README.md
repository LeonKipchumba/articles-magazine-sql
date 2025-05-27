# Articles Magazine SQL Code Challenge

This project is a simple magazine article management system built with Python and SQLite. It demonstrates object-oriented programming, database interaction, and basic CRUD operations for managing authors, magazines, and articles.

## Features

- **Author, Magazine, and Article Models**: Each with methods for creation, retrieval, and relationship management.
- **SQLite Database**: Data is persisted using SQLite, with schema and seed scripts provided.
- **Unit Tests**: Comprehensive test suite using `pytest` to validate all core functionality and relationships.

## Project Structure

```
code-challenge/
├── lib/
│   ├── db/
│   │   ├── connection.py
│   │   ├── schema.sql
│   │   ├── seed.py
│   ├── models/
│   │   ├── article.py
│   │   ├── author.py
│   │   ├── magazine.py
├── scripts/
│   ├── run_queries.py
│   ├── setup_db.py
├── tests/
│   ├── test_article.py
│   ├── test_author.py
│   ├── test_magazine.py
├── README.md
```

This project is for educational purposes.