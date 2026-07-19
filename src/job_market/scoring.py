import pandas as pd

CORE_SKILL_POINTS: dict[str, int] = {
    "python": 3,
    "aws": 3,
    "docker": 2,
    "linux": 2,
    "sql": 2,
    "terraform": 2,
    "kubernetes": 2,
    "ci/cd": 2,
    "github actions": 2,
}


def _get_text(row: pd.Series, column: str) -> str:
    """Return a normalized string value from a job posting row."""
    value = row.get(column, "")
    return value.casefold().strip() if isinstance(value, str) else ""


def _get_skills(row: pd.Series, column: str) -> set[str]:
    """Return normalized, semicolon-separated skills from a job posting row."""
    return {
        skill.strip().casefold()
        for skill in _get_text(row, column).split(";")
        if skill.strip()
    }


def _get_scoring_points(row: pd.Series) -> list[int]:
    """Return the point values for every matching priority rule."""
    scoring_points: list[int] = []
    location = _get_text(row, "location")
    work_mode = _get_text(row, "work_mode")
    job_type = _get_text(row, "job_type")
    title = _get_text(row, "title")

    if "kansas city" in location:
        scoring_points.append(3)
    if "missouri" in location:
        scoring_points.append(2)
    elif "kansas" in location:
        scoring_points.append(2)
    if work_mode in {"remote", "hybrid"}:
        scoring_points.append(1)
    if job_type in {"internship", "new grad", "junior", "entry-level"}:
        scoring_points.append(2)

    title_groups = (
        (("cloud", "devops", "infrastructure", "sre", "platform"), 3),
        (("python", "backend", "software", "data", "ai", "ml", "mlops"), 2),
    )
    for keywords, point_value in title_groups:
        if any(keyword in title for keyword in keywords):
            scoring_points.append(point_value)

    required_skills = _get_skills(row, "required_skills")
    for skill, point_value in CORE_SKILL_POINTS.items():
        if skill in required_skills:
            scoring_points.append(point_value)

    preferred_skills = _get_skills(row, "preferred_skills")
    for skill in CORE_SKILL_POINTS:
        if skill in preferred_skills:
            scoring_points.append(1)

    return scoring_points


def calculate_priority_score(row: pd.Series) -> int:
    """Calculate the rule-based priority score for one job posting."""
    return sum(_get_scoring_points(row))


def get_priority_level(score: int) -> str:
    """Map a numeric score to a dashboard priority level."""
    if score >= 10:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


def add_priority_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of job postings with rule-based priority columns."""
    scored_jobs = df.copy()
    scored_jobs["priority_score"] = scored_jobs.apply(calculate_priority_score, axis=1)
    scored_jobs["priority_level"] = scored_jobs["priority_score"].map(
        get_priority_level
    )
    return scored_jobs
