from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.auth import router as auth_router
from app.api.users import router as user_router
from app.api.job_postings import router as job_posting_router
from app.api.job_applications import router as job_application_router
from app.api.job_feedbacks import router as job_feedback_router
from app.api.outreach_templates import router as outreach_router
from app.api.trust_score import router as trust_score_router
from app.api.job_search import router as job_search_router
from app.api.resume import router as resume_router

settings = get_settings()

app = FastAPI(
    title="JobScout AI API",
    description="AI-powered job authenticity scoring, crowdsourced signals, and personalized outreach for job seekers.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["Auth"])
app.include_router(user_router, tags=["Users"])
app.include_router(job_posting_router, tags=["Job Postings"])
app.include_router(job_application_router, tags=["Job Applications"])
app.include_router(job_feedback_router, tags=["Job Feedbacks"])
app.include_router(outreach_router, tags=["Outreach"])
app.include_router(trust_score_router, tags=["Trust Score"])
app.include_router(job_search_router, tags=["Job Search"])
app.include_router(resume_router, tags=["Resume"])


@app.get("/health")
def health():
    return {"status": "ok"}
