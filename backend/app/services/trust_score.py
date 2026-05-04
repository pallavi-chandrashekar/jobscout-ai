from datetime import datetime, timezone

from app.models.models import JobPosting, JobFeedback
from app.schemas.schemas import TrustScoreDetail


OUTCOME_WEIGHTS = {
    "hired": 1.0,
    "interviewed": 0.8,
    "rejected": 0.1,
    "no_response": -0.2,
    "ghosted": -0.6,
    "fake": -1.0,
}

RED_FLAGS = [
    "urgently hiring", "too good to be true", "earn $$$",
    "work from home $", "no experience needed", "guaranteed income",
    "be your own boss", "unlimited earning", "make money fast",
]

TRUSTED_SOURCES = ["linkedin", "indeed", "glassdoor", "lever", "greenhouse", "workday"]


def _freshness_score(posted_date: datetime | None, is_active: bool) -> int:
    """Score 0-25 based on how fresh the posting is."""
    if not is_active:
        return 0
    if not posted_date:
        return 10
    now = datetime.now(timezone.utc)
    if posted_date.tzinfo is None:
        days_old = (now.replace(tzinfo=None) - posted_date).days
    else:
        days_old = (now - posted_date).days
    if days_old <= 7:
        return 25
    if days_old <= 14:
        return 22
    if days_old <= 30:
        return 18
    if days_old <= 60:
        return 12
    if days_old <= 90:
        return 6
    return 2


def _feedback_score(feedbacks: list[JobFeedback]) -> int:
    """Score 0-35 based on crowdsourced feedback outcomes."""
    if not feedbacks:
        return 17  # neutral
    total_weight = sum(OUTCOME_WEIGHTS.get(f.outcome, 0) for f in feedbacks)
    normalized = total_weight / len(feedbacks)  # -1.0 to 1.0
    return max(0, min(35, int(17.5 + (normalized * 17.5))))


def _company_score(company: str | None, company_url: str | None) -> int:
    """Score 0-15 based on company information presence."""
    score = 0
    if company and len(company) > 2:
        score += 5
    if company_url:
        score += 5
    if company and len(company) > 2 and company_url:
        score += 5
    return score


def _quality_score(job: JobPosting) -> int:
    """Score 0-25 based on posting quality heuristics."""
    score = 0
    if job.salary_min or job.salary_max:
        score += 8
    if job.title and len(job.title) > 5:
        score += 4
    if job.location:
        score += 3
    if job.description and len(job.description) > 100:
        score += 5

    text = f"{job.title or ''} {job.description or ''}".lower()
    flag_count = sum(1 for flag in RED_FLAGS if flag in text)
    score -= flag_count * 3

    if job.source and job.source.lower() in TRUSTED_SOURCES:
        score += 5

    return max(0, min(25, score))


def compute_trust_score(job: JobPosting, feedbacks: list[JobFeedback]) -> TrustScoreDetail:
    """Compute composite trust score (0-100) from 4 sub-scores."""
    f = _freshness_score(job.posted_date, job.is_active)
    fb = _feedback_score(feedbacks)
    c = _company_score(job.company, job.company_url)
    q = _quality_score(job)
    total = f + fb + c + q
    confidence = "high" if len(feedbacks) >= 10 else "medium" if len(feedbacks) >= 3 else "low"

    return TrustScoreDetail(
        freshness_score=f,
        feedback_score=fb,
        company_score=c,
        quality_score=q,
        total=total,
        confidence=confidence,
    )
