"""Job scraper service using python-jobspy to fetch real listings from LinkedIn, Indeed, Glassdoor."""

from datetime import datetime
from uuid import uuid4

from app.models.models import JobPosting
from app.services.trust_score import compute_trust_score


def scrape_jobs(
    search_term: str,
    location: str | None = None,
    remote: bool = False,
    results_wanted: int = 20,
    sources: list[str] | None = None,
) -> list[dict]:
    """Scrape job listings from multiple job boards."""
    from jobspy import scrape_jobs as jobspy_scrape

    site_names = sources or ["indeed", "linkedin", "glassdoor"]
    country = "USA"

    try:
        df = jobspy_scrape(
            site_name=site_names,
            search_term=search_term,
            location=location or "Remote" if remote else location,
            results_wanted=results_wanted,
            country_indeed=country,
            is_remote=remote,
        )
    except Exception as e:
        print(f"Scrape error: {e}")
        return []

    jobs = []
    for _, row in df.iterrows():
        job = {
            "url": str(row.get("job_url", "")),
            "title": str(row.get("title", "")) or None,
            "company": str(row.get("company", "")) or None,
            "company_url": str(row.get("company_url", "")) if row.get("company_url") else None,
            "location": str(row.get("location", "")) or None,
            "description": str(row.get("description", ""))[:5000] if row.get("description") else None,
            "source": str(row.get("site", "")).lower() or None,
            "salary_min": _parse_salary(row.get("min_amount")),
            "salary_max": _parse_salary(row.get("max_amount")),
            "salary_currency": str(row.get("currency", "USD")) if row.get("currency") else "USD",
            "posted_date": _parse_date(row.get("date_posted")),
            "is_active": True,
        }
        if job["url"]:
            jobs.append(job)

    return jobs


def import_scraped_jobs(db, jobs: list[dict]) -> dict:
    """Import scraped jobs into the database, skipping duplicates. Returns stats."""
    added = 0
    skipped = 0

    for job_data in jobs:
        url = job_data.get("url", "")
        if not url:
            skipped += 1
            continue

        existing = db.query(JobPosting).filter(JobPosting.url == url).first()
        if existing:
            skipped += 1
            continue

        job = JobPosting(id=uuid4(), **job_data)
        db.add(job)
        db.flush()

        # Compute initial trust score (no feedbacks yet)
        score = compute_trust_score(job, [])
        job.trust_score = score.total
        job.trust_score_updated_at = datetime.utcnow()

        added += 1

    db.commit()
    return {"added": added, "skipped": skipped, "total": len(jobs)}


def _parse_salary(value) -> int | None:
    if value is None:
        return None
    try:
        val = float(value)
        if val > 0:
            return int(val)
    except (ValueError, TypeError):
        pass
    return None


def _parse_date(value) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value))
    except (ValueError, TypeError):
        pass
    return None
