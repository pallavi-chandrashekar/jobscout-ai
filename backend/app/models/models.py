from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from app.db.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    class Config:
        orm_mode = True

    applications = relationship("JobApplication", back_populates="user")
    feedbacks = relationship("JobFeedback", back_populates="user")


class JobPosting(Base):
    __tablename__ = "job_postings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    url = Column(String, unique=True, nullable=False)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    source = Column(String)
    trust_score = Column(Integer)
    posted_date = Column(DateTime)
    is_active = Column(Boolean, default=True)

    feedbacks = relationship("JobFeedback", back_populates="job")
    applications = relationship("JobApplication", back_populates="job")


class JobApplication(Base):
    __tablename__ = "job_applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_postings.id"))
    status = Column(String)
    applied_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="applications")
    job = relationship("JobPosting", back_populates="applications")


class JobFeedback(Base):
    __tablename__ = "job_feedbacks"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_postings.id"))
    outcome = Column(String)
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
    created_at = Column(DateTime, default=datetime.utcnow)
