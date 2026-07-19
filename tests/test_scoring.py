import pandas as pd

from job_market.scoring import (
    add_priority_scores,
    calculate_priority_score,
    get_priority_level,
    get_priority_reasons,
)


def test_high_priority_kansas_city_cloud_python_aws_job() -> None:
    job = pd.Series(
        {
            "location": "Kansas City, Missouri",
            "work_mode": "Hybrid",
            "job_type": "Entry-Level",
            "title": "Cloud Backend Engineer",
            "required_skills": "Python;AWS;Docker",
            "preferred_skills": "Kubernetes",
        },
    )

    assert calculate_priority_score(job) == 22
    assert get_priority_level(calculate_priority_score(job)) == "High"
    assert "location (Kansas City) (+3)" in get_priority_reasons(job)
    assert "required_skills (Python) (+3)" in get_priority_reasons(job)


def test_low_priority_unrelated_job() -> None:
    job = pd.Series(
        {
            "location": "Denver, Colorado",
            "work_mode": "Onsite",
            "job_type": "Senior",
            "title": "Marketing Manager",
            "required_skills": "Communication;Excel",
            "preferred_skills": "Figma",
        },
    )

    assert calculate_priority_score(job) == 0
    assert get_priority_level(calculate_priority_score(job)) == "Low"
    assert get_priority_reasons(job) == []


def test_scoring_matches_case_insensitively() -> None:
    job = pd.Series(
        {
            "location": "KANSAS CITY, kansas",
            "work_mode": "REMOTE",
            "job_type": "junior",
            "title": "DEVOPS PLATFORM ENGINEER",
            "required_skills": "pYtHoN;aws;DOCKER",
            "preferred_skills": "KUBERNETES",
        },
    )

    assert calculate_priority_score(job) == 20


def test_missing_values_do_not_crash_scoring() -> None:
    job = pd.Series(
        {
            "location": None,
            "work_mode": pd.NA,
            "job_type": float("nan"),
            "title": None,
            "required_skills": pd.NA,
            "preferred_skills": None,
        },
    )

    assert calculate_priority_score(job) == 0
    assert get_priority_reasons(job) == []


def test_add_priority_scores_adds_columns_without_mutating_input() -> None:
    jobs = pd.DataFrame(
        [
            {
                "location": "Kansas City, Missouri",
                "work_mode": "Remote",
                "job_type": "Internship",
                "title": "Cloud Engineer",
                "required_skills": "Python;AWS",
                "preferred_skills": "Docker",
            },
        ],
    )
    original_columns = jobs.columns.tolist()

    scored_jobs = add_priority_scores(jobs)

    assert {"priority_score", "priority_level", "priority_reasons"}.issubset(
        scored_jobs.columns,
    )
    assert jobs.columns.tolist() == original_columns
    assert "priority_score" not in jobs.columns
