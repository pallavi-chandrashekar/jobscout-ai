from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.schemas import OutreachTemplateCreate, OutreachTemplateRead
from app.models.models import OutreachTemplate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/outreach-templates", response_model=OutreachTemplateRead)
def create_outreach_template(template: OutreachTemplateCreate, db: Session = Depends(get_db)):
    db_template = OutreachTemplate(**template.dict())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.get("/outreach-templates", response_model=list[OutreachTemplateRead])
def get_outreach_templates(db: Session = Depends(get_db)):
    return db.query(OutreachTemplate).all()
