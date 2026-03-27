.PHONY: dev
dev:
	@bun run dev

.PHONY: ci-install
ci-install:
	@bun install --frozen-lockfile

.PHONY: build
build:
	@bun run build

.PHONY: start
start:
	@bun run start

.PHONY: lint
lint:
	@bun run lint

.PHONY: check
check: lint

.PHONY: ci-check
ci-check: check
