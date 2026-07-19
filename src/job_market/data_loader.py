from pathlib import Path

import pandas as pd
from pandas.errors import EmptyDataError

REQUIRED_COLUMNS: tuple[str, ...] = (
    "company",
    "title",
    "location",
    "work_mode",
    "job_type",
    "domain",
    "required_skills",
    "preferred_skills",
    "date_posted",
    "apply_url",
    "status",
    "notes",
)


class CSVSchemaError(ValueError):
    """Raised when a job posting CSV does not match the expected schema."""


def load_job_postings(csv_path: str | Path) -> pd.DataFrame:
    """Load job postings from a CSV file and validate the required columns."""
    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    try:
        jobs = pd.read_csv(path)
    except EmptyDataError as error:
        raise CSVSchemaError(f"CSV file is empty: {path}") from error

    validate_required_columns(jobs)
    return jobs


def validate_required_columns(jobs: pd.DataFrame) -> None:
    """Ensure a DataFrame contains every required job posting column."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in jobs.columns]

    if missing_columns:
        missing = ", ".join(missing_columns)
        raise CSVSchemaError(f"Missing required CSV columns: {missing}")
