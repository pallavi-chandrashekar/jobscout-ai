from pydantic import BaseModel, EmailStr
from typing import Optional, Generic, TypeVar
from uuid import UUID
from datetime import datetime
from enum import Enum

T = TypeVar("T")


# --- Enums ---

class OutcomeEnum(str, Enum):
    interviewed = "interviewed"
    ghosted = "ghosted"
    fake = "fake"
    hired = "hired"
    no_response = "no_response"
    rejected = "rejected"


class OutreachType(str, Enum):
    cover_letter = "cover_letter"
    recruiter_message = "recruiter_message"
    follow_up = "follow_up"


class ToneEnum(str, Enum):
    professional = "professional"
    casual = "casual"
    enthusiastic = "enthusiastic"


# --- Pagination ---

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int


# --- Auth ---

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- User ---

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserRead(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# --- Job Posting ---

class JobPostingBase(BaseModel):
    url: str
    title: Optional[str] = None
    company: Optional[str] = None
    company_url: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = None
    posted_date: Optional[datetime] = None
    is_active: Optional[bool] = True


class JobPostingCreate(JobPostingBase):
    pass


class JobPostingUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    company_url: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = None
    posted_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class JobPostingRead(JobPostingBase):
    id: UUID
    trust_score: Optional[int] = None
    trust_score_updated_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Trust Score ---

class TrustScoreDetail(BaseModel):
    freshness_score: int
    feedback_score: int
    company_score: int
    quality_score: int
    total: int
    confidence: str


class JobPostingWithScore(JobPostingRead):
    trust_detail: Optional[TrustScoreDetail] = None


# --- Job Application ---

class JobApplicationBase(BaseModel):
    status: Optional[str] = "applied"
    applied_date: Optional[datetime] = None


class JobApplicationCreate(JobApplicationBase):
    job_id: UUID
    tailored_resume: Optional[str] = None
    cover_letter: Optional[str] = None


class JobApplicationUpdate(BaseModel):
    status: Optional[str] = None
    tailored_resume: Optional[str] = None
    cover_letter: Optional[str] = None


class JobApplicationRead(JobApplicationBase):
    id: UUID
    user_id: UUID
    job_id: UUID
    tailored_resume: Optional[str] = None
    cover_letter: Optional[str] = None

    class Config:
        from_attributes = True


# --- Job Feedback ---

class JobFeedbackCreate(BaseModel):
    job_id: UUID
    outcome: OutcomeEnum
    comment: Optional[str] = None
    tag: Optional[str] = None


class JobFeedbackRead(BaseModel):
    id: UUID
    job_id: UUID
    user_id: UUID
    outcome: str
    comment: Optional[str] = None
    tag: Optional[str] = None
    feedback_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class FeedbackAggregation(BaseModel):
    total_feedbacks: int
    outcome_counts: dict[str, int]
    confidence: str


# --- Outreach ---

class OutreachTemplateCreate(BaseModel):
    job_id: UUID
    message: str


class OutreachTemplateRead(BaseModel):
    id: UUID
    user_id: UUID
    job_id: UUID
    message: str
    outreach_type: Optional[str] = None
    tone: Optional[str] = None
    provider: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OutreachGenerateRequest(BaseModel):
    job_id: UUID
    outreach_type: OutreachType = OutreachType.cover_letter
    tone: ToneEnum = ToneEnum.professional
    resume_summary: Optional[str] = None


class OutreachGenerateResponse(BaseModel):
    message: str
    provider: str
    model: str
    tokens_used: int
