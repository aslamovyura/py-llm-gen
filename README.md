# Py-LLM-Gen

A clean architecture Python project for database search, built with Python 3.12.

## Project Structure

The project follows clean architecture principles with the following layers:

```
src/
├── domain/           # Core business logic and entities
│   ├── entities/     # Business objects
│   ├── repositories/ # Repository interfaces
│   └── services/     # Domain services
├── application/      # Use cases and business rules
│   ├── use_cases/    # Business use cases
│   ├── dto/          # Data Transfer Objects
│   └── services/     # Application services
├── infrastructure/   # External implementations
│   ├── database/     # Database adapters
│   ├── api/          # External API clients
│   └── repositories/ # Repository implementations
└── interface/       # User interaction
    ├── api/         # REST/GraphQL endpoints
    ├── web/         # Web interface
    └── cli/         # Command line interface
```

## Setup

1. Install Poetry:
```bash
pip install poetry
```

2. Install dependencies:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

## Development

- Format code:
```bash
poetry run black .
poetry run isort .
```

- Run tests:
```bash
poetry run pytest
```

- Type checking:
```bash
poetry run mypy .
```

- Linting:
```bash
poetry run flake8
```

## Database Population

The project includes a script to populate the database with test data. Before running the script, ensure that:

1. PostgreSQL is running and accessible
2. The database connection details in `.env` are correct
3. The database exists and is accessible

To populate the database with test data:

```bash
# Set PYTHONPATH to include the project root
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the populate script
python src/infrastructure/database/scripts/populate_db.py
```

The script will create:
- 10 users with different roles (admin, manager, user)
- 20 clients
- 30 pieces of equipment
- Multiple requests for each client
- Multiple offers for each request

## License

MIT
