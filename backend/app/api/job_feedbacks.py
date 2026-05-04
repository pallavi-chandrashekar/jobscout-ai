from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from collections import Counter
from datetime import datetime

from app.dependencies import get_db, get_current_user
from app.models.models import JobFeedback, JobPosting, User
from app.schemas.schemas import JobFeedbackCreate, JobFeedbackRead, FeedbackAggregation

router = APIRouter(prefix="/job-feedbacks")


@router.post("", response_model=JobFeedbackRead)
def create_feedback(
    feedback: JobFeedbackCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    job = db.query(JobPosting).filter(JobPosting.id == feedback.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")

    db_feedback = JobFeedback(
        user_id=user.id,
        job_id=feedback.job_id,
        outcome=feedback.outcome.value,
        comment=feedback.comment,
        tag=feedback.tag,
    )
    db.add(db_feedback)

    # Recompute trust score after new feedback
    from app.services.trust_score import compute_trust_score
    all_feedbacks = db.query(JobFeedback).filter(JobFeedback.job_id == feedback.job_id).all()
    all_feedbacks.append(db_feedback)
    score_detail = compute_trust_score(job, all_feedbacks)
    job.trust_score = score_detail.total
    job.trust_score_updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@router.get("", response_model=list[JobFeedbackRead])
def list_feedbacks(job_id: UUID | None = None, db: Session = Depends(get_db)):
    query = db.query(JobFeedback)
    if job_id:
        query = query.filter(JobFeedback.job_id == job_id)
    return query.order_by(JobFeedback.feedback_date.desc()).all()


@router.get("/aggregation/{job_id}", response_model=FeedbackAggregation)
def get_feedback_aggregation(job_id: UUID, db: Session = Depends(get_db)):
    feedbacks = db.query(JobFeedback).filter(JobFeedback.job_id == job_id).all()
    outcome_counts = dict(Counter(f.outcome for f in feedbacks))
    total = len(feedbacks)
    confidence = "high" if total >= 10 else "medium" if total >= 3 else "low"
    return FeedbackAggregation(
        total_feedbacks=total, outcome_counts=outcome_counts, confidence=confidence,
    )
