# Database Migrations Guide

This guide explains how to create and manage database migrations in the project using Alembic.

## Prerequisites

- PostgreSQL database running (in this project, it's running in a Docker container)
- Python environment with required dependencies installed
- Access to the database with proper credentials

## Project Structure

The database migration files are located in:
```
src/infrastructure/database/
├── alembic.ini           # Alembic configuration file
├── config.py            # Database configuration
├── models.py            # SQLAlchemy models
└── migrations/          # Migration files
    ├── env.py          # Migration environment configuration
    └── versions/       # Generated migration files
```

## Configuration

The database connection settings are stored in `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://postgres:StrongPassw@rd123@localhost:5433/equipment_db
DB_HOST=localhost
DB_PORT=5433
DB_NAME=equipment_db
DB_USER=postgres
DB_PASSWORD=StrongPassw@rd123
```

## Creating a New Migration

1. Make changes to your SQLAlchemy models in `src/infrastructure/database/models.py`

2. Generate a new migration:
```bash
cd src/infrastructure/database
alembic revision --autogenerate -m "description of changes"
```

This will create a new migration file in `migrations/versions/` with a timestamp and your description.

3. Review the generated migration file to ensure it contains the expected changes.

4. Apply the migration:
```bash
alembic upgrade head
```

## Common Migration Commands

- Create a new migration:
  ```bash
  alembic revision --autogenerate -m "description"
  ```

- Apply all pending migrations:
  ```bash
  alembic upgrade head
  ```

- Rollback one migration:
  ```bash
  alembic downgrade -1
  ```

- Rollback to a specific migration:
  ```bash
  alembic downgrade <revision_id>
  ```

- Show current migration status:
  ```bash
  alembic current
  ```

- Show migration history:
  ```bash
  alembic history
  ```

## Best Practices

1. **Always Review Generated Migrations**
   - Check the generated migration file before applying it
   - Ensure it contains the expected changes
   - Verify that no sensitive data is included

2. **Use Meaningful Migration Names**
   - Be descriptive in your migration messages
   - Include the purpose of the changes
   - Example: "add_user_phone_number" instead of "update_models"

3. **Keep Migrations Small and Focused**
   - Each migration should do one thing
   - Avoid combining multiple unrelated changes
   - Makes rollbacks easier and safer

4. **Test Migrations**
   - Test migrations in a development environment first
   - Verify both upgrade and downgrade paths
   - Ensure data integrity is maintained

5. **Backup Before Migrating**
   - Always backup your database before applying migrations
   - This is especially important in production environments

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify database credentials in `.env`
   - Ensure the database server is running
   - Check network connectivity

2. **Migration Conflicts**
   - If you encounter conflicts, you may need to:
     - Resolve the conflicts manually
     - Create a new migration that handles the conflict
     - In extreme cases, you might need to reset the migration history

3. **Failed Migrations**
   - If a migration fails:
     - Check the error message
     - Review the migration file
     - Consider rolling back to a known good state
     - Fix the issue and create a new migration

## Example Workflow

1. Make model changes:
```python
# models.py
class User(Base):
    __tablename__ = "users"
    # ... existing fields ...
    phone_number = Column(String(20), nullable=True)  # New field
```

2. Generate migration:
```bash
alembic revision --autogenerate -m "add_user_phone_number"
```

3. Review the generated migration file

4. Apply the migration:
```bash
alembic upgrade head
```

5. Verify the changes in the database

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) 