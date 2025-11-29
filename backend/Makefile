MANAGE := poetry run python manage.py
PORT ?= 8000

# ------------------------------
# install dependents
# ------------------------------
.PHONY: install
install:
	@poetry install

.PHONY: build
build:
	@poetry install --only main

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
	@poetry run uvicorn myproject.asgi:application --reload --host 0.0.0.0 --port $(PORT)

.PHONY: start
start: migrate
	@poetry run gunicorn -w 5 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$(PORT) myproject.asgi:application

# ------------------------------
# Pre-commit
# ------------------------------
.PHONY: pre-commit-install
pre-commit-install:
	@poetry run pre-commit install

.PHONY: pre-commit-run
pre-commit-run:
	@poetry run pre-commit run --files $(shell find apps api -type f -name "*.py")

# ------------------------------
# Formatters/linters
# ------------------------------

.PHONY: format
format:
	@poetry run black apps api
	@poetry run isort apps api

.PHONY: lint
lint:
	@poetry run flake8 apps api

.PHONY: type
type:
	@poetry run mypy apps api

.PHONY: check
check: format lint type