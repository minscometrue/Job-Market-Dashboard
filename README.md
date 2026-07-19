# Job Market Dashboard

A personal job market intelligence dashboard for tracking, analyzing, and prioritizing internship and entry-level job postings.

This project starts as a small Python-based MVP and is designed to gradually evolve into a more automated, data-driven job search system with job posting analysis, skill frequency tracking, priority scoring, AI-assisted insights, and cloud deployment.

## Project Purpose

The goal of this project is to build a practical dashboard that helps track job opportunities and understand the job market for roles such as:

* Python Software Engineer
* Backend Engineer
* Software Engineer
* DevOps Engineer
* Cloud Engineer
* Infrastructure Engineer
* Site Reliability Engineer
* Data Engineer
* AI / ML / MLOps Engineer

The first MVP focuses on manually collected job postings stored in a CSV file. Later versions may include database storage, automation, AI analysis, and deployment to cloud infrastructure.

## Current MVP Scope

The initial MVP should stay intentionally small.

### MVP Goals

* Load job posting data from a CSV file.
* Validate the required CSV columns.
* Analyze job postings using Python and pandas.
* Display a simple dashboard using Streamlit.
* Track common skills across job postings.
* Prioritize jobs using a simple rule-based scoring system.

### Non-Goals for the Initial MVP

The following should not be implemented in the first version:

* Web scraping
* AI analysis
* User authentication
* PostgreSQL
* FastAPI backend
* React frontend
* Docker deployment
* AWS deployment
* CI/CD pipeline

These may be added later after the basic local dashboard works.

## Tech Stack

| Area            | Technology | Reason                                                                     |
| --------------- | ---------- | -------------------------------------------------------------------------- |
| Language        | Python     | Good fit for data analysis, automation, AI integration, and DevOps tooling |
| Package Manager | uv         | Fast and simple Python dependency management                               |
| Data Analysis   | pandas     | Used for CSV loading, filtering, aggregation, and skill frequency analysis |
| Dashboard       | Streamlit  | Allows building a web dashboard quickly using Python only                  |
| Data Storage    | CSV        | Simple starting point before introducing a database                        |
| Testing         | pytest     | Used for testing data loading and analysis functions                       |
| Lint / Format   | ruff       | Used for linting, formatting, and import cleanup                           |
| Type Checking   | mypy       | Used for static type checking                                              |
| Command Runner  | Makefile   | Provides consistent project commands                                       |

## Project Structure

```text
job-market-dashboard/
├── app/
│   └── main.py
├── data/
│   └── raw/
├── src/
│   └── job_market/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── analyzer.py
│       └── scoring.py
├── tests/
│   └── test_data_loader.py
├── .gitignore
├── Makefile
├── pyproject.toml
├── README.md
└── uv.lock
```

## Directory Responsibilities

### `app/`

Contains the Streamlit web application entry point.

The main dashboard should start from:

```text
app/main.py
```

This file should focus on UI composition only. Business logic should be imported from `src/job_market/`.

### `src/job_market/`

Contains reusable project logic.

Expected responsibilities:

* `data_loader.py`

  * Load job posting data from CSV.
  * Validate required columns.
  * Return a pandas DataFrame.

* `analyzer.py`

  * Analyze job posting data.
  * Count jobs by location, company, domain, and status.
  * Calculate skill frequency.

* `scoring.py`

  * Assign priority scores to job postings.
  * Keep the scoring logic rule-based for the MVP.

### `data/raw/`

Stores manually collected raw job posting CSV files.

For the MVP, CSV files may be committed to Git if they contain only sample or public job posting data.

Do not commit private notes, personal data, secrets, API keys, or sensitive information.

### `tests/`

Contains automated tests.

Initial test focus:

* CSV file loading
* Required column validation
* Empty file handling
* Skill parsing
* Job scoring logic

## Expected CSV Schema

The initial CSV file should use the following columns:

```csv
company,title,location,work_mode,job_type,domain,required_skills,preferred_skills,date_posted,apply_url,status,notes
```

### Column Descriptions

| Column             | Description                                                                         |
| ------------------ | ----------------------------------------------------------------------------------- |
| `company`          | Company name                                                                        |
| `title`            | Job title                                                                           |
| `location`         | Job location                                                                        |
| `work_mode`        | Onsite, Hybrid, Remote, or Unknown                                                  |
| `job_type`         | Internship, Entry-Level, New Grad, Junior, or Unknown                               |
| `domain`           | Industry or job domain, such as Healthcare, FinTech, Cloud, AI, Data, Manufacturing |
| `required_skills`  | Semicolon-separated required skills                                                 |
| `preferred_skills` | Semicolon-separated preferred skills                                                |
| `date_posted`      | Posting date if available                                                           |
| `apply_url`        | Application URL                                                                     |
| `status`           | Tracking status                                                                     |
| `notes`            | Personal notes about the posting                                                    |

### Skill Format

Skills should be separated by semicolons.

Example:

```csv
Python;SQL;AWS;Docker
```

This format is easier to parse than comma-separated skills because job descriptions often contain commas inside text.

## Suggested Job Status Values

Use consistent status values:

```text
New
Interested
Applied
Interview
Rejected
Closed
Saved
Ignored
```

## Development Commands

This project uses `uv` and `Makefile`.

### Install dependencies

```bash
make install
```

Equivalent command:

```bash
uv sync
```

### Run the Streamlit app

```bash
make run
```

Equivalent command:

```bash
uv run streamlit run app/main.py
```

### Run lint checks

```bash
make lint
```

Equivalent command:

```bash
uv run ruff check .
```

### Format code

```bash
make format
```

Equivalent command:

```bash
uv run ruff format .
```

### Run type checks

```bash
make type
```

Equivalent command:

```bash
uv run mypy src
```

### Run tests

```bash
make test
```

Equivalent command:

```bash
uv run pytest
```

### Run all checks

```bash
make check
```

This should run lint, type checks, and tests.

## Recommended Makefile

```makefile
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
```

Makefile commands must use tab indentation, not spaces.

## Git Workflow

This project uses a simple GitHub Flow style workflow.

### Branch Strategy

```text
main = stable working version
feature branches = isolated work for each meaningful task
```

Examples:

```text
chore/project-setup
feat/csv-schema
feat/data-loader
feat/skill-analysis
feat/priority-scoring
feat/dashboard-mvp
docs/update-readme
fix/csv-path
```

### Commit Message Style

Use Conventional Commit style:

```text
chore: set up Python project structure
feat: add CSV data loader
feat: add skill frequency analysis
feat: add priority scoring rules
test: add data loader tests
docs: update README
fix: handle missing CSV file
```

## Development Guidelines

Keep the MVP simple.

Before adding a new tool, framework, or service, check whether it directly supports the current MVP goal.

### Preferred Approach

* Start with CSV before database.
* Start with rule-based scoring before AI scoring.
* Start with Streamlit before FastAPI or React.
* Start local before Docker or AWS deployment.
* Keep business logic inside `src/job_market/`.
* Keep Streamlit UI code inside `app/main.py`.
* Add tests for reusable functions.
* Run `make check` before merging to `main`.

### Avoid in Early MVP

* Do not add scraping yet.
* Do not add authentication yet.
* Do not add cloud deployment yet.
* Do not add a backend API yet.
* Do not hardcode absolute local paths.
* Do not put analysis logic directly inside the Streamlit UI file.

## Planned Roadmap

### Phase 1: Local MVP

* Define CSV schema.
* Add sample job posting CSV.
* Implement CSV data loader.
* Validate required columns.
* Add skill parsing.
* Add basic skill frequency analysis.
* Add rule-based priority scoring.
* Display results in Streamlit.

### Phase 2: Improved Dashboard

* Add sidebar filters.
* Add job status filters.
* Add skill frequency chart.
* Add priority ranking table.
* Add summary metrics.
* Improve README with screenshots.

### Phase 3: Data Management

* Add manual job entry form.
* Add duplicate detection.
* Move from CSV to SQLite or PostgreSQL.
* Track job status changes over time.

### Phase 4: Automation

* Add semi-automated job posting collection.
* Parse job alert emails or saved job feeds.
* Detect new postings.
* Avoid duplicate postings.
* Add scheduled update workflow.

### Phase 5: AI Analysis

* Summarize job descriptions.
* Extract required skills from job descriptions.
* Compare job requirements against personal skill targets.
* Generate job fit explanations.
* Suggest resume keywords.

### Phase 6: Cloud / DevOps Portfolio Extension

* Add Dockerfile.
* Add GitHub Actions CI.
* Deploy dashboard to AWS.
* Store data in managed database or object storage.
* Add logging and monitoring.
* Optionally manage infrastructure using Terraform.

## Codex / Coding Agent Instructions

When working on this project, follow these rules:

1. Keep changes small and focused.
2. Do not introduce unnecessary frameworks.
3. Do not skip the MVP sequence.
4. Do not put business logic inside `app/main.py`.
5. Prefer simple functions over complex classes in the early phase.
6. Add or update tests when adding reusable logic.
7. Preserve the `src/job_market/` package structure.
8. Use `uv` commands instead of raw `pip` commands.
9. Use `make check` before considering a task complete.
10. Explain any structural change in the commit message or pull request description.

## Current Status

The project is currently in the setup and MVP planning phase.

The next expected task is to define the initial CSV schema and add a small sample CSV file under:

```text
data/raw/job_postings.csv
```

After the sample CSV exists, the next implementation target should be:

```text
src/job_market/data_loader.py
```

The first useful function should load the CSV file, validate required columns, and return a pandas DataFrame.
