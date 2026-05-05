from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel

from app.dependencies import get_db, get_current_user
from app.models.models import JobPosting, User
from app.services.resume_tailor import tailor_resume

router = APIRouter(prefix="/resume")


class TailorRequest(BaseModel):
    job_id: UUID
    resume_text: str


class TailorResponse(BaseModel):
    tailored_resume: str
    cover_letter: str
    provider: str
    model: str
    tokens_used: int


@router.post("/tailor", response_model=TailorResponse)
async def tailor_resume_for_job(
    request: TailorRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    job = db.query(JobPosting).filter(JobPosting.id == request.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")

    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty")

    result = await tailor_resume(
        resume_text=request.resume_text,
        job=job,
    )

    return TailorResponse(**result)


@router.post("/tailor-upload", response_model=TailorResponse)
async def tailor_resume_upload(
    job_id: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Upload a resume file (.txt, .md) and tailor it for a job."""
    job = db.query(JobPosting).filter(JobPosting.id == UUID(job_id)).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")

    content = await resume.read()
    resume_text = content.decode("utf-8")

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume file is empty")

    result = await tailor_resume(resume_text=resume_text, job=job)

    return TailorResponse(**result)
