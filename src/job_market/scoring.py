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


def _get_scoring_rules(row: pd.Series) -> list[tuple[str, int]]:
    """Return every matching scoring rule and its point value."""
    rules: list[tuple[str, int]] = []
    skill_names = {
        "python": "Python",
        "aws": "AWS",
        "docker": "Docker",
        "linux": "Linux",
        "sql": "SQL",
        "terraform": "Terraform",
        "kubernetes": "Kubernetes",
        "ci/cd": "CI/CD",
        "github actions": "GitHub Actions",
    }
    title_keyword_names = {
        "cloud": "Cloud",
        "devops": "DevOps",
        "infrastructure": "Infrastructure",
        "sre": "SRE",
        "platform": "Platform",
        "python": "Python",
        "backend": "Backend",
        "software": "Software",
        "data": "Data",
        "ai": "AI",
        "ml": "ML",
        "mlops": "MLOps",
    }
    location = _get_text(row, "location")
    work_mode = _get_text(row, "work_mode")
    job_type = _get_text(row, "job_type")
    title = _get_text(row, "title")

    if "kansas city" in location:
        rules.append(("location (Kansas City)", 3))
    if "missouri" in location:
        rules.append(("location (Missouri)", 2))
    elif "kansas" in location:
        rules.append(("location (Kansas)", 2))
    if work_mode in {"remote", "hybrid"}:
        rules.append((f"work_mode ({work_mode.title()})", 1))
    if job_type in {"internship", "new grad", "junior", "entry-level"}:
        rules.append((f"job_type ({job_type.title()})", 2))

    title_groups = (
        (("cloud", "devops", "infrastructure", "sre", "platform"), 3),
        (("python", "backend", "software", "data", "ai", "ml", "mlops"), 2),
    )
    for keywords, points in title_groups:
        matching_keywords = [keyword for keyword in keywords if keyword in title]
        if matching_keywords:
            matched_value = ", ".join(
                title_keyword_names[keyword] for keyword in matching_keywords
            )
            rules.append((f"title ({matched_value})", points))

    required_skills = _get_skills(row, "required_skills")
    for skill, points in CORE_SKILL_POINTS.items():
        if skill in required_skills:
            rules.append((f"required_skills ({skill_names[skill]})", points))

    preferred_skills = _get_skills(row, "preferred_skills")
    for skill in CORE_SKILL_POINTS:
        if skill in preferred_skills:
            rules.append((f"preferred_skills ({skill_names[skill]})", 1))

    return rules


def calculate_priority_score(row: pd.Series) -> int:
    """Calculate the rule-based priority score for one job posting."""
    return sum(points for _, points in _get_scoring_rules(row))


def get_priority_level(score: int) -> str:
    """Map a numeric score to a dashboard priority level."""
    if score >= 10:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


def get_priority_reasons(row: pd.Series) -> list[str]:
    """Return human-readable rules that contributed to a job's score."""
    return [f"{reason} (+{points})" for reason, points in _get_scoring_rules(row)]


def add_priority_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of job postings with rule-based priority columns."""
    scored_jobs = df.copy()
    scored_jobs["priority_score"] = scored_jobs.apply(calculate_priority_score, axis=1)
    scored_jobs["priority_level"] = scored_jobs["priority_score"].map(
        get_priority_level
    )
    scored_jobs["priority_reasons"] = scored_jobs.apply(
        lambda row: (
            "; ".join(get_priority_reasons(row)) or "No matching priority rules"
        ),
        axis=1,
    )
    return scored_jobs
