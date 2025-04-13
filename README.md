# DB Search Project

A Python-based project implementing clean architecture principles for searching deals in a database.

## Project Structure

```
.
├── src/
│   ├── domain/           # Domain layer containing business logic and entities
│   ├── application/      # Application layer with use cases
│   ├── infrastructure/   # Infrastructure layer with database adapters
│   └── api/             # API layer for user interaction
├── tests/               # Test directory mirroring src structure
├── pyproject.toml       # Poetry project configuration
└── README.md           # Project documentation
```

## Layers

- **Domain Layer**: Contains business logic, entities, and interfaces
- **Application Layer**: Implements use cases and orchestrates domain logic
- **Infrastructure Layer**: Provides concrete implementations of interfaces
- **API Layer**: Handles user interaction and request/response formatting

## Prerequisites

- Python 3.9 or higher
- Poetry (Python package manager)

## Setup

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository and install dependencies:
```bash
git clone <repository-url>
cd db-search
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

## Development

### Code Quality Tools

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Static type checking
- **ruff**: Fast Python linter
- **bandit**: Security linter
- **safety**: Dependency security checker

### Development Commands

Format code:
```bash
poetry run black src/ tests/
poetry run isort src/ tests/
```

Run linters:
```bash
poetry run ruff check src/ tests/
poetry run mypy src/
poetry run bandit -r src/
poetry run safety check
```

Run tests with coverage:
```bash
poetry run pytest
```

### Pre-commit Hooks

Install pre-commit hooks:
```bash
poetry run pre-commit install
```

The pre-commit hooks will automatically run the following checks before each commit:
- Code formatting (black, isort)
- Linting (ruff)
- Type checking (mypy)
- Security checks (bandit)

## Running the Application

1. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

2. Start the FastAPI server:
```bash
poetry run uvicorn src.api.routes:app --reload
```

The API will be available at `http://localhost:8000`

## Database Migrations

To create and apply database migrations:
```bash
poetry run alembic revision --autogenerate -m "description"
poetry run alembic upgrade head
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run all quality checks
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
