import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIRECTORY = PROJECT_ROOT / "src"
if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from job_market.analyzer import calculate_skill_frequency  # noqa: E402
from job_market.data_loader import CSVSchemaError, load_job_postings  # noqa: E402
from job_market.scoring import add_priority_scores  # noqa: E402

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "job_postings.csv"
SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "sample_jobs.csv"


def get_data_path() -> Path:
    """Prefer the standard CSV path, with the existing sample as a fallback."""
    if DATA_PATH.exists() or not SAMPLE_DATA_PATH.exists():
        return DATA_PATH
    return SAMPLE_DATA_PATH


def get_filter_options(jobs: pd.DataFrame, column: str) -> list[str]:
    """Return sorted, non-empty filter values for a DataFrame column."""
    if column not in jobs.columns:
        return []

    values = jobs[column].dropna().astype(str)
    return sorted(value for value in values.unique() if value.strip())


def filter_jobs(jobs: pd.DataFrame) -> pd.DataFrame:
    """Apply the optional sidebar filters to job postings."""
    filtered_jobs = jobs.copy()
    selected_filters = {
        "status": st.sidebar.multiselect("Status", get_filter_options(jobs, "status")),
        "job_type": st.sidebar.multiselect(
            "Job type", get_filter_options(jobs, "job_type")
        ),
        "work_mode": st.sidebar.multiselect(
            "Work mode", get_filter_options(jobs, "work_mode")
        ),
        "priority_level": st.sidebar.multiselect(
            "Priority level", get_filter_options(jobs, "priority_level")
        ),
    }

    for column, selected_values in selected_filters.items():
        if selected_values:
            filtered_jobs = filtered_jobs[filtered_jobs[column].isin(selected_values)]

    skill_search = st.sidebar.text_input("Skill search")
    if skill_search:
        skill_columns = [
            column
            for column in ("required_skills", "preferred_skills")
            if column in filtered_jobs.columns
        ]
        if skill_columns:
            skills = (
                filtered_jobs[skill_columns]
                .fillna("")
                .astype(str)
                .agg(" ".join, axis=1)
            )
            filtered_jobs = filtered_jobs[
                skills.str.contains(skill_search, case=False, regex=False, na=False)
            ]

    return filtered_jobs


def count_matching_jobs(jobs: pd.DataFrame, column: str, value: str) -> int:
    """Count rows whose column contains a value, ignoring case and nulls."""
    if column not in jobs.columns:
        return 0
    return int(
        jobs[column].fillna("").astype(str).str.contains(value, case=False).sum()
    )


def main() -> None:
    """Render the Job Market Dashboard MVP."""
    st.set_page_config(page_title="Job Market Dashboard", layout="wide")
    st.title("Job Market Dashboard")
    st.caption("Track, prioritize, and explore internship and entry-level roles.")

    data_path = get_data_path()
    if data_path == SAMPLE_DATA_PATH:
        st.info("Using data/raw/sample_jobs.csv until job_postings.csv is available.")

    try:
        jobs = load_job_postings(data_path)
    except (FileNotFoundError, CSVSchemaError, pd.errors.ParserError) as error:
        st.error(f"Unable to load job posting data: {error}")
        return

    scored_jobs = add_priority_scores(jobs)
    filtered_jobs = filter_jobs(scored_jobs)

    total_jobs = len(filtered_jobs)
    interested_jobs = count_matching_jobs(filtered_jobs, "status", "Interested")
    applied_jobs = count_matching_jobs(filtered_jobs, "status", "Applied")
    high_priority_jobs = count_matching_jobs(filtered_jobs, "priority_level", "High")
    kansas_city_jobs = count_matching_jobs(filtered_jobs, "location", "Kansas City")

    metrics = st.columns(5)
    metrics[0].metric("Total jobs", total_jobs)
    metrics[1].metric("Interested", interested_jobs)
    metrics[2].metric("Applied", applied_jobs)
    metrics[3].metric("High priority", high_priority_jobs)
    metrics[4].metric("Kansas City", kansas_city_jobs)

    st.subheader("Job postings")
    table_columns = [
        "company",
        "title",
        "location",
        "work_mode",
        "job_type",
        "domain",
        "required_skills",
        "preferred_skills",
        "status",
        "priority_score",
        "priority_level",
        "apply_url",
    ]
    available_columns = [column for column in table_columns if column in filtered_jobs]
    st.dataframe(filtered_jobs[available_columns], hide_index=True, width="stretch")

    st.subheader("Top required skills")
    skill_frequency = calculate_skill_frequency(filtered_jobs)
    if skill_frequency.empty:
        st.info("No required skills are available for the selected jobs.")
    else:
        st.bar_chart(skill_frequency.head(10))


if __name__ == "__main__":
    main()
