from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.models import JobApplication as JobApplicationModel
from app.schemas.schemas import JobApplicationCreate, JobApplication
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/job-applications", response_model=JobApplication)
def create_application(application: JobApplicationCreate, db: Session = Depends(get_db)):
    job_app = JobApplicationModel(**application.dict())
    db.add(job_app)
    db.commit()
    db.refresh(job_app)
    return job_app

@router.get("/job-applications", response_model=list[JobApplication])
def get_applications(db: Session = Depends(get_db)):
    return db.query(JobApplicationModel).all()
