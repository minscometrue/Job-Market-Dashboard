# Job Market Dashboard

## Project Overview

Job Market Dashboard is a personal job market intelligence dashboard for
tracking, analyzing, and prioritizing internship and entry-level job postings.
It supports roles across Python, Software Engineering, Cloud, DevOps,
Infrastructure, Data, AI/ML, and MLOps.

The MVP uses a manually maintained CSV file, pandas-based analysis, and a
minimal Streamlit dashboard.

## Current MVP Features

- Load and validate job-posting CSV data.
- Analyze required and preferred skills.
- Apply rule-based priority scores and levels.
- Display summary metrics, a job table, and top-skill chart in Streamlit.
- Filter by status, job type, work mode, priority level, and skill text.
- Run locally, with Docker, or with Docker Compose.

## Tech Stack

Python, uv, pandas, Streamlit, pytest, ruff, mypy, Makefile, Docker, Docker
Compose, and CSV-based data storage.

## Project Structure

```text
job-market-dashboard/
├── app/main.py                  # Streamlit UI entry point
├── data/raw/                    # Manually maintained CSV data
├── src/job_market/
│   ├── data_loader.py            # CSV loading and validation
│   ├── analyzer.py               # Skill parsing and frequency analysis
│   └── scoring.py                # Rule-based priority scoring
├── tests/                        # Automated tests
├── Dockerfile
├── compose.yaml
├── Makefile
├── pyproject.toml
└── uv.lock
```

Keep UI orchestration in `app/main.py` and reusable business logic in
`src/job_market/`.

## CSV Schema

Create `data/raw/job_postings.csv` with the following columns:

```csv
company,title,location,work_mode,job_type,domain,required_skills,preferred_skills,date_posted,apply_url,status,notes
```

Skills must be semicolon-separated:

```text
Python;SQL;AWS;Docker
```

## Setup

```bash
uv sync
# or
make install
```

## Run Locally

```bash
make run
```

Equivalent command:

```bash
uv run streamlit run app/main.py
```

## Run with Docker

```bash
make docker-build
make docker-run
```

Equivalent commands:

```bash
docker build -t job-market-dashboard .
docker run --rm -p 8501:8501 job-market-dashboard
```

Open [http://localhost:8501](http://localhost:8501).

## Run with Docker Compose

```bash
make compose-up
make compose-ps
make compose-logs
make compose-down
```

Equivalent commands:

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f
docker compose down
```

Compose mounts the local `data/` directory at `/app/data`, so CSV changes are
available without rebuilding the image. The dashboard is available at
[http://localhost:8501](http://localhost:8501).

## Development Commands

```bash
make format
make lint
make type
make test
make check
```

## Git Workflow

- `main` is the stable branch.
- Use `feat/mvp` or focused feature branches for MVP work.
- Keep commits small and run `make check` before merging.

## Current Limitations

- CSV data is manually maintained.
- No scraping, AI analysis, database, authentication, or cloud deployment.

## Roadmap

1. Improve dashboard UI and charts.
2. Add duplicate detection and manual job entry.
3. Move to SQLite or PostgreSQL.
4. Add job-posting collection automation.
5. Add AI-assisted job-description analysis.
6. Add GitHub Actions, AWS deployment, monitoring, and logging.

## Coding Agent Guidelines

- Keep changes small and focused.
- Do not add unnecessary frameworks.
- Keep business logic out of `app/main.py`.
- Add tests for reusable logic in `src/job_market/`.
- Use `uv` and Makefile commands.
- Do not add scraping, AI, databases, cloud features, or other infrastructure
  beyond the explicitly requested scope.
