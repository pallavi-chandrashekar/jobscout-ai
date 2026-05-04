"""Seed the database with sample data for demo purposes."""

import sys
from datetime import datetime, timedelta
from uuid import uuid4

from app.config import get_settings
from app.db.database import engine, SessionLocal, Base
from app.models.models import User, JobPosting, JobFeedback, JobApplication
from app.services.auth import hash_password
from app.services.trust_score import compute_trust_score


def seed():
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Check if already seeded
    if db.query(User).count() > 0:
        print("Database already seeded, skipping.")
        db.close()
        return

    print("Seeding database...")

    # --- Demo User ---
    demo_user = User(
        id=uuid4(),
        email="demo@jobscout.ai",
        name="Demo User",
        password_hash=hash_password("demo1234"),
    )
    db.add(demo_user)

    # --- Job Postings ---
    now = datetime.utcnow()
    jobs = [
        JobPosting(
            id=uuid4(), url="https://linkedin.com/jobs/view/sr-data-engineer-acme",
            title="Senior Data Engineer", company="Acme Technologies",
            company_url="https://acmetech.com", location="San Francisco, CA",
            description="We're looking for a Senior Data Engineer to design and build scalable data pipelines. You'll work with Spark, Airflow, and dbt to process terabytes of data daily. Requirements: 5+ years experience with distributed systems, strong SQL, Python proficiency. We offer competitive salary, equity, and full benefits.",
            source="linkedin", salary_min=180000, salary_max=230000, salary_currency="USD",
            posted_date=now - timedelta(days=3), is_active=True,
        ),
        JobPosting(
            id=uuid4(), url="https://indeed.com/viewjob/ml-engineer-dataflow",
            title="ML Engineer - Platform", company="DataFlow Inc",
            company_url="https://dataflow.io", location="Remote",
            description="Join our ML Platform team to build the infrastructure that powers our AI products. You'll design feature stores, model serving pipelines, and experiment tracking systems. Experience with Kubernetes, MLflow, and PyTorch required.",
            source="indeed", salary_min=160000, salary_max=210000, salary_currency="USD",
            posted_date=now - timedelta(days=7), is_active=True,
        ),
        JobPosting(
            id=uuid4(), url="https://linkedin.com/jobs/view/eng-manager-cloudnova",
            title="Engineering Manager - Data Platform", company="CloudNova",
            company_url="https://cloudnova.com", location="Seattle, WA",
            description="Lead a team of 8 engineers building our next-generation data platform. You'll own the technical roadmap, mentor engineers, and drive cross-functional alignment. We're looking for someone with 3+ years of management experience and deep technical expertise in data systems.",
            source="linkedin", salary_min=220000, salary_max=280000, salary_currency="USD",
            posted_date=now - timedelta(days=5), is_active=True,
        ),
        JobPosting(
            id=uuid4(), url="https://glassdoor.com/job-listing/backend-dev-startupx",
            title="Backend Developer", company="StartupX",
            location="Austin, TX",
            description="Fast-paced startup looking for a backend developer. Node.js and Python experience preferred.",
            source="glassdoor", posted_date=now - timedelta(days=14), is_active=True,
        ),
        JobPosting(
            id=uuid4(), url="https://linkedin.com/jobs/view/data-analyst-megacorp",
            title="Data Analyst", company="MegaCorp",
            company_url="https://megacorp.com", location="New York, NY",
            description="Entry-level data analyst position. You'll create dashboards, write SQL queries, and present findings to stakeholders. Experience with Tableau or Looker preferred. Bachelor's degree required.",
            source="linkedin", salary_min=85000, salary_max=110000, salary_currency="USD",
            posted_date=now - timedelta(days=2), is_active=True,
        ),
        JobPosting(
            id=uuid4(), url="https://indeed.com/viewjob/urgently-hiring-remote",
            title="URGENTLY HIRING - Work From Home - Earn $$$ Daily!",
            company="QuickCash LLC",
            location="Remote",
            description="Be your own boss! No experience needed. Guaranteed income of $5000/week. This is a once in a lifetime opportunity. Unlimited earning potential!",
            source="indeed", posted_date=now - timedelta(days=45), is_active=True,
        ),
        JobPosting(
            id=uuid4(), url="https://linkedin.com/jobs/view/swe-techgiant",
            title="Software Engineer II", company="TechGiant",
            company_url="https://techgiant.com", location="Mountain View, CA",
            description="Build and maintain large-scale distributed systems serving billions of requests per day. Strong understanding of system design, algorithms, and data structures required. 3+ years of experience with Java, Go, or C++.",
            source="linkedin", salary_min=150000, salary_max=200000, salary_currency="USD",
            posted_date=now - timedelta(days=10), is_active=True,
        ),
        JobPosting(
            id=uuid4(), url="https://indeed.com/viewjob/stale-devops-posting",
            title="DevOps Engineer", company="OldTech Solutions",
            location="Chicago, IL",
            description="Looking for a DevOps engineer.",
            source="indeed", posted_date=now - timedelta(days=120), is_active=False,
        ),
        JobPosting(
            id=uuid4(), url="https://linkedin.com/jobs/view/ai-lead-neuroai",
            title="AI/ML Lead", company="NeuroAI Labs",
            company_url="https://neuroai.dev", location="Boston, MA",
            description="Lead our AI research and engineering team. You'll set the technical direction for our NLP and computer vision products, hire and mentor a team of 5 researchers, and publish at top conferences. PhD in CS/ML preferred. Strong publication record a plus.",
            source="linkedin", salary_min=250000, salary_max=350000, salary_currency="USD",
            posted_date=now - timedelta(days=1), is_active=True,
        ),
        JobPosting(
            id=uuid4(), url="https://glassdoor.com/job-listing/fullstack-webworks",
            title="Full Stack Developer", company="WebWorks Agency",
            company_url="https://webworks.dev", location="Remote",
            description="We're a small agency looking for a full stack developer to join our team. You'll work on client projects using React, Node.js, and PostgreSQL. Collaborative team environment with flexible hours.",
            source="glassdoor", salary_min=120000, salary_max=155000, salary_currency="USD",
            posted_date=now - timedelta(days=8), is_active=True,
        ),
    ]

    for job in jobs:
        db.add(job)
    db.flush()

    # --- Feedbacks ---
    feedback_data = [
        # Acme - great company
        (jobs[0].id, "hired"), (jobs[0].id, "interviewed"), (jobs[0].id, "interviewed"),
        (jobs[0].id, "interviewed"), (jobs[0].id, "no_response"),
        # DataFlow - decent
        (jobs[1].id, "interviewed"), (jobs[1].id, "no_response"), (jobs[1].id, "rejected"),
        # CloudNova - great
        (jobs[2].id, "hired"), (jobs[2].id, "interviewed"), (jobs[2].id, "interviewed"),
        # StartupX - ghosted a lot
        (jobs[3].id, "ghosted"), (jobs[3].id, "ghosted"), (jobs[3].id, "no_response"),
        # QuickCash - fake
        (jobs[5].id, "fake"), (jobs[5].id, "fake"), (jobs[5].id, "fake"),
        (jobs[5].id, "fake"), (jobs[5].id, "ghosted"),
        # TechGiant - mixed
        (jobs[6].id, "interviewed"), (jobs[6].id, "rejected"), (jobs[6].id, "no_response"),
        # OldTech - ghosted
        (jobs[7].id, "ghosted"), (jobs[7].id, "ghosted"),
        # NeuroAI - new, one feedback
        (jobs[8].id, "interviewed"),
        # WebWorks - good
        (jobs[9].id, "hired"), (jobs[9].id, "interviewed"),
    ]

    for job_id, outcome in feedback_data:
        fb = JobFeedback(
            id=uuid4(), user_id=demo_user.id, job_id=job_id,
            outcome=outcome, feedback_date=now - timedelta(hours=len(feedback_data)),
        )
        db.add(fb)

    db.flush()

    # --- Compute trust scores ---
    for job in jobs:
        feedbacks = db.query(JobFeedback).filter(JobFeedback.job_id == job.id).all()
        score = compute_trust_score(job, feedbacks)
        job.trust_score = score.total
        job.trust_score_updated_at = now

    # --- Demo applications ---
    for job in [jobs[0], jobs[2], jobs[8]]:
        app = JobApplication(
            id=uuid4(), user_id=demo_user.id, job_id=job.id,
            status="applied", applied_date=now - timedelta(days=2),
        )
        db.add(app)

    db.commit()
    db.close()

    print(f"Seeded: 1 user, {len(jobs)} jobs, {len(feedback_data)} feedbacks, 3 applications")
    print("Login: demo@jobscout.ai / demo1234")


if __name__ == "__main__":
    seed()
