from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.models import JobPosting as JobPostingModel
from app.schemas.schemas import JobPostingCreate, JobPosting

router = APIRouter()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/job-postings", response_model=JobPosting)
def create_job_posting(posting: JobPostingCreate, db: Session = Depends(get_db)):
    job = JobPostingModel(**posting.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.get("/job-postings", response_model=list[JobPosting])
def get_job_postings(db: Session = Depends(get_db)):
    return db.query(JobPostingModel).all()
