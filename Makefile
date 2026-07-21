.PHONY: install run lint format type test check docker-build docker-run

install:
	uv sync

run:
	uv run streamlit run app/main.py

docker-build:
	docker build -t job-market-dashboard .

docker-run:
	docker run --rm -p 8501:8501 job-market-dashboard

lint:
	uv run ruff check .

format:
	uv run ruff format .

type:
	uv run mypy src

test:
	uv run pytest

check: lint type test
