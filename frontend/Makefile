# --------------------
# Variables
# --------------------
PNPM = pnpm
NODE_ENV ?= development

# --------------------
# Install deps
# --------------------
install:
	$(PNPM) install

# --------------------
# Dev / Build
# --------------------
dev:
	$(PNPM) dev

build:
	$(PNPM) build

start:
	NODE_ENV=production $(PNPM) start

# --------------------
# Quality tools
# --------------------
lint:
	$(PNPM) lint

lint-fix:
	$(PNPM) lint --fix

format:
	$(PNPM) prettier --write .

typecheck:
	$(PNPM) tsc --noEmit

# --------------------
# Clean
# --------------------
clean:
	rm -rf .next node_modules dist