# OneMore

[![Backend CI](https://github.com/Kostyanuch-c/OneMore/actions/workflows/backend.yml/badge.svg)](https://github.com/Kostyanuch-c/OneMore/actions/workflows/backend.yml)
[![Frontend CI](https://github.com/Kostyanuch-c/OneMore/actions/workflows/frontend.yml/badge.svg)](https://github.com/Kostyanuch-c/OneMore/actions/workflows/frontend.yml)
[![Deploy](https://github.com/Kostyanuch-c/OneMore/actions/workflows/deploy.yml/badge.svg)](https://github.com/Kostyanuch-c/OneMore/actions/workflows/deploy.yml)

Monorepo for the **KhimRepetitor** learning platform.

The project has two parts:
- `backend/` - Django + Django Ninja API.
- `frontend/` - Next.js + HeroUI client.

## Quick Start

### 1. Backend

```bash
cd backend
cp .env_example .env
make install
make migrate
make dev
```

API docs are available at `http://localhost:8000/api/docs`.

### 2. Frontend

Open a second terminal:

```bash
cd frontend
bun install
make dev
```

Frontend starts at `http://localhost:3000`.

## Useful Commands

Backend:
- `make test` - run all tests.
- `make test-unit` - run unit tests only.
- `make test-integration` - run integration tests only.
- `make test-api` - run API tests.
- `make check` - format, lint, and type checks.

Frontend:
- `make lint` - run ESLint with autofix.
- `make build` - build for production.
- `make start` - start production build.
