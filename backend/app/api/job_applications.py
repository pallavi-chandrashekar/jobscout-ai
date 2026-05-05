from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies import get_db, get_current_user
from app.models.models import JobApplication, User
from app.schemas.schemas import JobApplicationCreate, JobApplicationRead, JobApplicationUpdate

router = APIRouter(prefix="/job-applications")


@router.post("", response_model=JobApplicationRead)
def create_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    job_app = JobApplication(
        user_id=user.id,
        job_id=application.job_id,
        status=application.status or "applied",
        applied_date=application.applied_date,
        tailored_resume=application.tailored_resume,
        cover_letter=application.cover_letter,
    )
    db.add(job_app)
    db.commit()
    db.refresh(job_app)
    return job_app


@router.get("", response_model=list[JobApplicationRead])
def list_my_applications(
    db: Session = Depends(get_db), user: User = Depends(get_current_user),
):
    return db.query(JobApplication).filter(JobApplication.user_id == user.id).all()


@router.get("/{app_id}", response_model=JobApplicationRead)
def get_application(app_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    app = db.query(JobApplication).filter(JobApplication.id == app_id, JobApplication.user_id == user.id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


@router.put("/{app_id}", response_model=JobApplicationRead)
def update_application(
    app_id: UUID, update: JobApplicationUpdate,
    db: Session = Depends(get_db), user: User = Depends(get_current_user),
):
    app = db.query(JobApplication).filter(JobApplication.id == app_id, JobApplication.user_id == user.id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if update.status is not None:
        app.status = update.status
    db.commit()
    db.refresh(app)
    return app


@router.delete("/{app_id}", status_code=204)
def delete_application(app_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    app = db.query(JobApplication).filter(JobApplication.id == app_id, JobApplication.user_id == user.id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(app)
    db.commit()
