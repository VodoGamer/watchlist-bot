.PHONY: prepare migration-generate migration-upgrade watchlist-bot

PYTHON := .venv/bin/python3

prepare:
	uv sync

migration-generate:
	@test -n "$(MSG)" || (echo "Error: MSG not set. Usage: make migration-generate MSG=\"Migration name\"" && exit 1)
	$(PYTHON) -m alembic revision --autogenerate -m "$(MSG)"

migration-upgrade:
	$(PYTHON) -m alembic upgrade head

watchlist-bot:
	uv run watchlist-bot
