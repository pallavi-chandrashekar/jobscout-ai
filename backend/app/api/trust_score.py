from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.dependencies import get_db
from app.models.models import JobPosting, JobFeedback
from app.schemas.schemas import TrustScoreDetail
from app.services.trust_score import compute_trust_score

router = APIRouter(prefix="/trust-score")


@router.get("/{job_id}", response_model=TrustScoreDetail)
def get_trust_score(job_id: UUID, db: Session = Depends(get_db)):
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    feedbacks = db.query(JobFeedback).filter(JobFeedback.job_id == job_id).all()
    return compute_trust_score(job, feedbacks)


@router.post("/{job_id}/refresh", response_model=TrustScoreDetail)
def refresh_trust_score(job_id: UUID, db: Session = Depends(get_db)):
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    feedbacks = db.query(JobFeedback).filter(JobFeedback.job_id == job_id).all()
    score_detail = compute_trust_score(job, feedbacks)
    job.trust_score = score_detail.total
    job.trust_score_updated_at = datetime.utcnow()
    db.commit()
    return score_detail
