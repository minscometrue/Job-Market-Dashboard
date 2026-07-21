.PHONY: install run lint format type test check compose-build compose-up compose-down compose-logs compose-ps

install:
	uv sync

run:
	uv run streamlit run app/main.py

compose-build:
	docker compose build

compose-up:
	docker compose up -d --build

compose-down:
	docker compose down

compose-logs:
	docker compose logs -f

compose-ps:
	docker compose ps

lint:
	uv run ruff check .

format:
	uv run ruff format .

type:
	uv run mypy src

test:
	uv run pytest

check: lint type test
