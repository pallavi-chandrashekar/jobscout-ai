from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies import get_db, get_current_user
from app.models.models import OutreachTemplate, JobPosting, User
from app.schemas.schemas import (
    OutreachTemplateCreate, OutreachTemplateRead,
    OutreachGenerateRequest, OutreachGenerateResponse,
)

router = APIRouter(prefix="/outreach")


@router.post("/templates", response_model=OutreachTemplateRead)
def create_template(
    template: OutreachTemplateCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_template = OutreachTemplate(
        user_id=user.id, job_id=template.job_id, message=template.message,
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


@router.get("/templates", response_model=list[OutreachTemplateRead])
def list_templates(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(OutreachTemplate).filter(
        OutreachTemplate.user_id == user.id
    ).order_by(OutreachTemplate.created_at.desc()).all()


@router.post("/generate", response_model=OutreachGenerateResponse)
async def generate_outreach(
    request: OutreachGenerateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    job = db.query(JobPosting).filter(JobPosting.id == request.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")

    from app.services.outreach import generate_outreach_message
    result = await generate_outreach_message(
        job=job, outreach_type=request.outreach_type.value,
        tone=request.tone.value, resume_summary=request.resume_summary,
    )

    db_template = OutreachTemplate(
        user_id=user.id, job_id=request.job_id, message=result.message,
        outreach_type=request.outreach_type.value, tone=request.tone.value,
        provider=result.provider,
    )
    db.add(db_template)
    db.commit()
    return result
