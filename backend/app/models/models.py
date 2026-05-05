from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship("JobApplication", back_populates="user")
    feedbacks = relationship("JobFeedback", back_populates="user")


class JobPosting(Base):
    __tablename__ = "job_postings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    url = Column(String, unique=True, nullable=False, index=True)
    title = Column(String)
    company = Column(String)
    company_url = Column(String, nullable=True)
    location = Column(String)
    description = Column(Text, nullable=True)
    source = Column(String)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(3), nullable=True)
    trust_score = Column(Integer, nullable=True)
    trust_score_updated_at = Column(DateTime, nullable=True)
    posted_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    feedbacks = relationship("JobFeedback", back_populates="job")
    applications = relationship("JobApplication", back_populates="job")


class JobApplication(Base):
    __tablename__ = "job_applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_postings.id"))
    status = Column(String, default="applied")
    applied_date = Column(DateTime, default=datetime.utcnow)
    tailored_resume = Column(Text, nullable=True)
    cover_letter = Column(Text, nullable=True)

    user = relationship("User", back_populates="applications")
    job = relationship("JobPosting", back_populates="applications")


class JobFeedback(Base):
    __tablename__ = "job_feedbacks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_postings.id"))
    outcome = Column(String, nullable=False)
    feedback_date = Column(DateTime, default=datetime.utcnow)
    comment = Column(Text, nullable=True)
    tag = Column(String(50), nullable=True)

    user = relationship("User", back_populates="feedbacks")
    job = relationship("JobPosting", back_populates="feedbacks")


class OutreachTemplate(Base):
    __tablename__ = "outreach_templates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_postings.id"))
    message = Column(Text)
    outreach_type = Column(String, default="cover_letter")
    tone = Column(String, default="professional")
    provider = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
