from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.dependencies import get_db, get_current_user
from app.models.models import User
from app.services.job_scraper import scrape_jobs, import_scraped_jobs

router = APIRouter(prefix="/job-search")


class SearchRequest(BaseModel):
    query: str
    location: str | None = None
    remote: bool = False
    results_wanted: int = 20
    sources: list[str] | None = None


class SearchResponse(BaseModel):
    added: int
    skipped: int
    total: int
    message: str


@router.post("/scrape", response_model=SearchResponse)
def search_and_import(
    request: SearchRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Scrape job listings from job boards and import into database."""
    jobs = scrape_jobs(
        search_term=request.query,
        location=request.location,
        remote=request.remote,
        results_wanted=request.results_wanted,
        sources=request.sources,
    )

    if not jobs:
        return SearchResponse(added=0, skipped=0, total=0, message="No jobs found. Try different search terms.")

    stats = import_scraped_jobs(db, jobs)

    return SearchResponse(
        added=stats["added"],
        skipped=stats["skipped"],
        total=stats["total"],
        message=f"Found {stats['total']} jobs. Added {stats['added']} new, skipped {stats['skipped']} duplicates.",
    )
