# Articles Management System

This project models the relationships between authors, articles, and magazines using a SQL database. It provides a structured way to manage and query data related to authors and their contributions to various magazines through articles.

## Project Structure

```
code-challenge/
├── lib/                # Main code directory
│   ├── models/         # Model classes for Authors, Articles, and Magazines
│   ├── db/             # Database components including connection and schema
│   ├── controllers/     # Optional: Business logic
│   ├── debug.py        # Interactive debugging
│   └── __init__.py     # Makes lib a package
├── tests/              # Test directory for unit tests
├── scripts/            # Helper scripts for database setup and queries
├── .gitignore          # Files and directories to be ignored by Git
└── README.md           # Project documentation
```

## Features

- **Author Management**: Create, retrieve, and manage authors and their articles.
- **Magazine Management**: Create, retrieve, and manage magazines and their published articles.
- **Article Management**: Create, retrieve, and manage articles, linking them to authors and magazines.
- **Relationships**: Support for many-to-many relationships between authors and magazines.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd code-challenge
   ```

2. **Set up the virtual environment**:
   - Using Pipenv:
     ```
     pipenv install pytest sqlite3
     pipenv shell
     ```
   - Using venv:
     ```
     python -m venv env
     source env/bin/activate  # Mac/Linux
     env\Scripts\activate     # Windows
     pip install pytest
     ```

3. **Set up the database**:
   - Run the setup script to create the database schema and seed initial data:
     ```
     python scripts/setup_db.py
     ```

4. **Run tests**:
   - Execute tests to ensure everything is working correctly:
     ```
     pytest
     ```

## Usage

- Use the provided scripts in the `scripts` directory to interact with the database and run queries.
- The `lib` directory contains the core functionality, including models and database connections.

## Contribution

Feel free to fork the repository and submit pull requests for any improvements or features you would like to add. 

## License

This project is open-source and available under the MIT License.