.PHONY: install run lint format type test check

install:
	uv sync

run:
	uv run streamlit run app/main.py

lint:
	uv run ruff check .

format:
	uv run ruff format .

type:
	uv run mypy src

test:
	uv run pytest

check: lint type test