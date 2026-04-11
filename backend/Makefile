MANAGE := uv run python src/manage.py
PORT ?= 8000

.PHONY: install
install:
	@uv sync

.PHONY: ci-install
ci-install:
	@uv sync --frozen

.PHONY: build
build:
	@uv sync --no-dev

.PHONY: superuser
superuser:
	@$(MANAGE) createsuperuser

.PHONY: create_migrations
create_migrations:
	@$(MANAGE) makemigrations

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

.PHONY: dev
dev:
	@uv run uvicorn project.asgi:application --reload --host 0.0.0.0 --port $(PORT) --app-dir src

.PHONY: start
start:
	@uv run gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$(PORT) src.project.asgi:application

.PHONY: pre-commit-install
pre-commit-install:
	@uv run pre-commit install

.PHONY: pre-commit-run
pre-commit-run:
	@uv run pre-commit run --files $(shell find src/apps src/api -type f -name "*.py")

.PHONY: format
format:
	@uv run ruff format src/apps src/api tests

.PHONY: lint
lint:
	@uv run ruff check src/apps src/api tests

.PHONY: lint-fix
lint-fix:
	@uv run ruff check --fix --unsafe-fixes src/apps src/api tests

.PHONY: type
type:
	@MYPYPATH=src uv run mypy src/apps src/api

.PHONY: test
test:
	@uv run pytest $(opts) $(path)

.PHONY: test-unit
test-unit:
	@uv run pytest -m unit

.PHONY: test-integration
test-integration:
	@uv run pytest -m integration

.PHONY: test-api
test-api:
	@uv run pytest -m api

.PHONY: check
check: format lint-fix lint type test

.PHONY: ci-migrations-check
ci-migrations-check:
	@uv run python src/manage.py makemigrations --check --dry-run

.PHONY: ci-check
ci-check: ci-migrations-check check
