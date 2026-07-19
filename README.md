# Job Market Dashboard

## Project Overview

Job Market Dashboard is a personal job market intelligence dashboard for
tracking, analyzing, and prioritizing internship and entry-level job postings.
It helps organize opportunities for Python, Software Engineering, Cloud,
DevOps, Infrastructure, Data, AI/ML, and MLOps roles.

The current MVP uses a manually maintained CSV file, pandas-based analysis, and
a small Streamlit dashboard. It is intentionally local and simple so that the
core job-search workflow is useful before automation or deployment features are
introduced.

## Current MVP Features

- Load job postings from a CSV file.
- Validate that required CSV columns are present.
- Parse and analyze required and preferred skills.
- Apply explainable, rule-based priority scoring.
- Display the results in a Streamlit dashboard.
- Filter jobs by status, job type, work mode, priority level, and skill search.
- Show summary metrics, a job table, and a top-required-skills chart.

## Tech Stack

| Area | Technology |
| --- | --- |
| Language | Python |
| Package manager | uv |
| Data analysis | pandas |
| Dashboard | Streamlit |
| Testing | pytest |
| Linting and formatting | ruff |
| Type checking | mypy |
| Command runner | Makefile |
| MVP data storage | CSV |

## Project Structure

```text
job-market-dashboard/
├── app/
│   └── main.py
├── data/
│   └── raw/
│       ├── job_postings.csv      # Standard local data file
│       └── sample_jobs.csv       # Included sample/fallback data
├── src/
│   └── job_market/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── data_loader.py
│       └── scoring.py
├── tests/
│   ├── test_data_loader.py
│   └── test_scoring.py
├── Makefile
├── pyproject.toml
├── README.md
└── uv.lock
```

- `app/main.py`: Streamlit UI composition, filters, metrics, and tables. Keep
  reusable business logic out of this file.
- `src/job_market/data_loader.py`: CSV loading and required-column validation.
- `src/job_market/analyzer.py`: Skill parsing and skill-frequency analysis.
- `src/job_market/scoring.py`: Rule-based job priority scores and levels.
- `data/raw/job_postings.csv`: Standard location for a manually maintained job
  posting CSV. The dashboard uses `sample_jobs.csv` as a fallback while the
  standard file is absent.
- `tests/`: Automated tests for reusable data-loading, analysis, and scoring
  behavior.

## CSV Schema

Create `data/raw/job_postings.csv` with these columns:

```csv
company,title,location,work_mode,job_type,domain,required_skills,preferred_skills,date_posted,apply_url,status,notes
```

| Column | Description |
| --- | --- |
| `company` | Company name |
| `title` | Job title |
| `location` | Job location |
| `work_mode` | Onsite, Hybrid, Remote, or Unknown |
| `job_type` | Internship, Entry-Level, New Grad, Junior, or Unknown |
| `domain` | Job or industry domain |
| `required_skills` | Required skills |
| `preferred_skills` | Preferred skills |
| `date_posted` | Posting date, if available |
| `apply_url` | Application URL |
| `status` | Tracking status, such as New, Interested, or Applied |
| `notes` | Personal notes |

Separate skills with semicolons:

```text
Python;SQL;AWS;Docker
```

## Setup

Install the project dependencies with either command:

```bash
uv sync
```

```bash
make install
```

## Running the Dashboard

Run the Streamlit dashboard from the project root:

```bash
make run
```

Equivalent command:

```bash
uv run streamlit run app/main.py
```

## Development Commands

```bash
make format  # Format code
make lint    # Run lint checks
make type    # Run type checks
make test    # Run tests
make check   # Run lint, type checks, and tests
```

## Git Workflow

- `main` is the stable branch.
- MVP work can happen on `feat/mvp` or focused feature branches.
- Use small, focused commits with clear messages.
- Run `make check` before merging to `main`.

## Current Limitations

- CSV data is manually maintained.
- No job-posting scraping yet.
- No AI analysis yet.
- No database yet.
- No authentication.
- No cloud deployment yet.

## Roadmap

1. Improve the dashboard UI and add better charts.
2. Add duplicate detection and a manual job-entry form.
3. Move data storage to SQLite or PostgreSQL.
4. Add automation for job posting collection.
5. Add AI-based job-description analysis.
6. Add Docker and GitHub Actions.
7. Deploy to AWS.
8. Add monitoring and logging.

## Coding Agent Guidelines

- Keep changes small and focused.
- Do not add unnecessary frameworks.
- Keep business logic out of `app/main.py`.
- Keep reusable logic in `src/job_market/`.
- Add tests when adding reusable logic.
- Use `uv` and `Makefile` commands for local development.
- Do not introduce scraping, AI, database, Docker, or cloud features unless
  explicitly requested.
