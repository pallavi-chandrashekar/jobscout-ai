from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
import math

from app.dependencies import get_db, get_current_user
from app.models.models import JobPosting, User
from app.schemas.schemas import (
    JobPostingCreate, JobPostingRead, JobPostingUpdate, PaginatedResponse,
)

router = APIRouter(prefix="/job-postings")


@router.post("", response_model=JobPostingRead)
def create_job_posting(
    posting: JobPostingCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    existing = db.query(JobPosting).filter(JobPosting.url == posting.url).first()
    if existing:
        raise HTTPException(status_code=400, detail="Job posting with this URL already exists")
    job = JobPosting(**posting.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("", response_model=PaginatedResponse[JobPostingRead])
def list_job_postings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    source: str | None = None,
    min_score: int | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(JobPosting)
    if search:
        query = query.filter(
            JobPosting.title.ilike(f"%{search}%") | JobPosting.company.ilike(f"%{search}%")
        )
    if source:
        query = query.filter(JobPosting.source == source)
    if min_score is not None:
        query = query.filter(JobPosting.trust_score >= min_score)
    if is_active is not None:
        query = query.filter(JobPosting.is_active == is_active)

    total = query.count()
    items = query.order_by(JobPosting.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedResponse(
        items=items, total=total, page=page, page_size=page_size,
        pages=math.ceil(total / page_size) if total > 0 else 0,
    )


@router.get("/{job_id}", response_model=JobPostingRead)
def get_job_posting(job_id: UUID, db: Session = Depends(get_db)):
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return job


@router.put("/{job_id}", response_model=JobPostingRead)
def update_job_posting(
    job_id: UUID, update: JobPostingUpdate,
    db: Session = Depends(get_db), user: User = Depends(get_current_user),
):
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=204)
def delete_job_posting(
    job_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user),
):
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    db.delete(job)
    db.commit()
