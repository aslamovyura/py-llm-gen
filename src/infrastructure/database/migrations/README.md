# Database Migrations

This directory contains database migration scripts managed by Alembic. These migrations help track and apply changes to the database schema over time.

## Setup

1. Make sure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

2. Ensure your database is running and the connection string in `src/infrastructure/database/config.py` is correct.

## Creating a New Migration

To create a new migration after making changes to your models:

```bash
alembic revision --autogenerate -m "description of changes"
```

This will create a new migration file in the `versions` directory.

## Running Migrations

To apply all pending migrations:

```bash
alembic upgrade head
```

To rollback the last migration:

```bash
alembic downgrade -1
```

To rollback to a specific version:

```bash
alembic downgrade <revision_id>
```

## Checking Migration Status

To see the current migration status:

```bash
alembic current
```

To see the migration history:

```bash
alembic history
```

## Important Notes

- Always review auto-generated migrations before applying them
- Never delete migration files once they've been applied to a production database
- Make sure to test migrations in a development environment before applying to production
- Keep migrations atomic and focused on a single change when possible 