from fastapi import FastAPI
from app.api.users import router as user_router
from app.api.job_postings import router as job_posting_router
from app.api.job_applications import router as job_application_router
from app.api.job_feedbacks import router as job_feedback_router
from app.api.outreach_templates import router as outreach_template_router

app = FastAPI(
    title="JobScout AI API",
    description="API backend for JobScout AI - helps users track, verify, and manage job applications effectively.",
    version="1.0.0"
)

# Register routers
app.include_router(user_router, tags=["Users"])
app.include_router(job_posting_router, tags=["Job Postings"])
app.include_router(job_application_router, tags=["Job Applications"])
app.include_router(job_feedback_router, tags=["Job Feedbacks"])
app.include_router(outreach_template_router, tags=["Outreach Templates"])
