# Backend

Backend service for the ChemRepetitor platform, built with Django.

## Stack

- Python 3.14
- Django 6
- Django Ninja
- PostgreSQL
- uv (dependency management and runtime)
- pytest, mypy, ruff

## Run Locally

```bash
cp .env_example .env
make install
make migrate
make dev
```

API docs are available at `http://localhost:8000/api/docs`.

## Main Commands

- `make dev` - run in development mode (Uvicorn).
- `make start` - run in production mode (Gunicorn + Uvicorn worker).
- `make create_migrations` - create migrations.
- `make migrate` - apply migrations.
- `make superuser` - create an admin user.

## Quality and Tests

- `make check` - formatting, linting, and type checks.
- `make test` - all tests.
- `make test-unit` - unit tests.
- `make test-integration` - integration tests.
- `make test-api` - API tests.
