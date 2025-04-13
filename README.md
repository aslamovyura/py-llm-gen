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

## License

MIT
