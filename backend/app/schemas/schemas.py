from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime


# ------------------------------
# User Schemas
# ------------------------------

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ------------------------------
# Job Posting Schemas
# ------------------------------

class JobPostingBase(BaseModel):
    url: str
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    source: Optional[str] = None
    trust_score: Optional[int] = None
    posted_date: Optional[datetime] = None
    is_active: Optional[bool] = True

class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    id: UUID

    class Config:
        from_attributes = True


# ------------------------------
# Job Application Schemas
# ------------------------------

class JobApplicationBase(BaseModel):
    status: Optional[str] = None
    applied_date: Optional[datetime] = None

class JobApplicationCreate(JobApplicationBase):
    user_id: UUID
    job_id: UUID

class JobApplication(JobApplicationBase):
    id: UUID
    user_id: UUID
    job_id: UUID

    class Config:
        from_attributes = True


# -------------------------------
# Job Feedback Schemas
# -------------------------------
class JobFeedbackCreate(BaseModel):
    job_id: UUID
    user_id: UUID
    outcome: Optional[str] = None

class JobFeedbackRead(BaseModel):
    id: UUID
    job_id: UUID
    user_id: UUID
    outcome: Optional[str] = None
    feedback_date: Optional[datetime] = None

    class Config:
        from_attributes = True

# -------------------------------
# Outreach Template Schemas
# -------------------------------
class OutreachTemplateCreate(BaseModel):
    user_id: UUID
    job_id: UUID
    message: str

class OutreachTemplateRead(BaseModel):
    id: UUID
    user_id: UUID
    job_id: UUID
    message: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True