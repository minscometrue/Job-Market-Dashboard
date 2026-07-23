.PHONY: install run lint format type test check docker-build docker-run compose-build compose-up compose-down compose-logs compose-ps

install:
	uv sync

run:
	uv run streamlit run app/main.py

docker-build:
	docker build -t job-market-dashboard .

docker-run:
	docker run --rm -p 8501:8501 job-market-dashboard

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

deploy:
	git pull
	docker compose up -d --build
	docker image prune -f

lint:
	uv run ruff check .

format:
	uv run ruff format .

type:
	uv run mypy src

test:
	uv run pytest

check: lint type test
