from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.schemas import JobFeedbackCreate, JobFeedbackRead
from app.models.models import JobFeedback

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/job-feedbacks", response_model=JobFeedbackRead)
def create_job_feedback(feedback: JobFeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = JobFeedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.get("/job-feedbacks", response_model=list[JobFeedbackRead])
def get_all_feedbacks(db: Session = Depends(get_db)):
    return db.query(JobFeedback).all()
