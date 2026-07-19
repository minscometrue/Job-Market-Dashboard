from collections import Counter

import pandas as pd


def parse_skills(skills: object) -> list[str]:
    """Convert a semicolon-separated skill value into clean skill names."""
    if not isinstance(skills, str):
        return []

    return [skill.strip() for skill in skills.split(";") if skill.strip()]


def calculate_skill_frequency(
    jobs: pd.DataFrame,
    *,
    include_preferred: bool = False,
) -> pd.Series:
    """Count how many job postings list each skill.

    Required skills are counted by default. Set ``include_preferred`` to also
    include skills listed as preferred qualifications.
    """
    skill_columns = ["required_skills"]
    if include_preferred:
        skill_columns.append("preferred_skills")

    frequencies: Counter[str] = Counter()
    for column in skill_columns:
        for value in jobs[column]:
            frequencies.update(set(parse_skills(value)))

    return pd.Series(frequencies, dtype="int64").sort_index().sort_values(
        ascending=False,
        kind="stable",
    )
