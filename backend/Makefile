MANAGE := uv run python manage.py
PORT ?= 8000

# ------------------------------
# install dependents
# ------------------------------
.PHONY: install
install:
	@uv sync

.PHONY: build
build:
	@uv sync --no-dev

# ------------------------------
# Data base
# ------------------------------
.PHONY: create_migrations
create_migrations:
	@$(MANAGE) makemigrations

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

# ------------------------------
# Django shell
# ------------------------------
.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

# ------------------------------
# Start project
# ------------------------------
.PHONY: dev
dev:
	@uv run uvicorn myproject.asgi:application --reload --host 0.0.0.0 --port $(PORT)

.PHONY: start
start: migrate
	@uv run gunicorn -w 5 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$(PORT) myproject.asgi:application

# ------------------------------
# Pre-commit
# ------------------------------
.PHONY: pre-commit-install
pre-commit-install:
	@uv run pre-commit install

.PHONY: pre-commit-run
pre-commit-run:
	@uv run pre-commit run --files $(shell find apps api -type f -name "*.py")

# ------------------------------
# Formatters/linters
# ------------------------------

.PHONY: format
format:
	@uv run ruff format apps api

.PHONY: lint
lint:
	@uv run ruff check apps api

.PHONY: lint-fix
lint-fix:
	@uv run ruff check --fix --unsafe-fixes apps api

.PHONY: type
type:
	@uv run mypy apps api

.PHONY: check
check: format lint-fix lint type