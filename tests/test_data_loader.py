from pathlib import Path

import pandas as pd
import pytest

from job_market.analyzer import calculate_skill_frequency, parse_skills
from job_market.data_loader import (
    CSVSchemaError,
    REQUIRED_COLUMNS,
    load_job_postings,
    validate_required_columns,
)


def write_csv(path: Path, rows: list[str]) -> None:
    path.write_text("\n".join(rows), encoding="utf-8")


def test_load_job_postings_reads_valid_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "jobs.csv"
    write_csv(
        csv_path,
        [
            ",".join(REQUIRED_COLUMNS),
            (
                "Acme Cloud,Junior Backend Engineer,Seattle WA,Hybrid,"
                "Entry-Level,Cloud,Python;SQL;Docker,AWS;Terraform,"
                "2026-07-01,https://example.com/acme-backend,Interested,"
                "Good Python backend fit"
            ),
        ],
    )

    jobs = load_job_postings(csv_path)

    assert list(jobs.columns) == list(REQUIRED_COLUMNS)
    assert len(jobs) == 1
    assert jobs.loc[0, "company"] == "Acme Cloud"


def test_load_job_postings_raises_for_missing_required_columns(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "jobs.csv"
    write_csv(
        csv_path,
        ["company,title", "Acme Cloud,Junior Backend Engineer"],
    )

    with pytest.raises(CSVSchemaError, match="Missing required CSV columns"):
        load_job_postings(csv_path)


def test_load_job_postings_raises_for_empty_file(tmp_path: Path) -> None:
    csv_path = tmp_path / "jobs.csv"
    csv_path.write_text("", encoding="utf-8")

    with pytest.raises(CSVSchemaError, match="CSV file is empty"):
        load_job_postings(csv_path)


def test_load_job_postings_raises_for_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_job_postings(tmp_path / "missing.csv")


def test_validate_required_columns_accepts_all_required_columns() -> None:
    jobs = pd.DataFrame(columns=REQUIRED_COLUMNS)

    validate_required_columns(jobs)


def test_parse_skills_strips_whitespace_and_ignores_empty_values() -> None:
    assert parse_skills(" Python ; SQL;; Docker ") == ["Python", "SQL", "Docker"]
    assert parse_skills(None) == []


def test_calculate_skill_frequency_counts_required_skills_per_job() -> None:
    jobs = pd.DataFrame(
        {
            "required_skills": ["Python; SQL; Python", "Python;Docker", None],
            "preferred_skills": ["AWS", "SQL;AWS", "Python"],
        },
    )

    frequencies = calculate_skill_frequency(jobs)

    assert frequencies.to_dict() == {"Python": 2, "Docker": 1, "SQL": 1}


def test_calculate_skill_frequency_can_include_preferred_skills() -> None:
    jobs = pd.DataFrame(
        {
            "required_skills": ["Python;SQL", "Python"],
            "preferred_skills": ["AWS", "SQL;AWS"],
        },
    )

    frequencies = calculate_skill_frequency(jobs, include_preferred=True)

    assert frequencies.to_dict() == {"AWS": 2, "Python": 2, "SQL": 2}
