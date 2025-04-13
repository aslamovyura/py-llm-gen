.PHONY: format lint test run

format:
	poetry run black src/ tests/
	poetry run isort src/ tests/

lint:
	poetry run flake8 src/ tests/
	poetry run mypy src/

test:
	poetry run pytest tests/

run:
	poetry run python src/main.py

install:
	poetry install 