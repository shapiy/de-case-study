# Initialize project
init:
    cp .env.example .env
    uv sync

# Database commands
db-up:
    docker compose up -d

db-down:
    docker compose down

db-reset:
    docker compose down -v
    docker compose up -d

# Django commands
migrate:
    uv run python manage.py migrate

makemigrations:
    uv run python manage.py makemigrations

seed:
    uv run python manage.py seed_transactions

# Development server
dev:
    uv run python manage.py runserver

# Utilities
shell:
    uv run python manage.py shell_plus

superuser:
    uv run python manage.py createsuperuser

# Testing and linting
test:
    uv run pytest apps/

lint:
    uv run ruff check .

format:
    uv run ruff format .

typecheck:
    uv run mypy .

# TODO: Add typecheck after mypy issues are fixed
check: lint

# Setup full project
setup: init db-up migrate seed
    @echo "Setup complete! Run 'just dev' to start the server"
