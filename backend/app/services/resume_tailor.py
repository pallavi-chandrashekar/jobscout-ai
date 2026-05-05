"""Resume tailoring service — uses LLM to customize resume for a specific job."""

from app.models.models import JobPosting
from app.llm.factory import create_llm_client, detect_provider


TAILOR_SYSTEM_PROMPT = """You are an expert resume writer and career coach.
Given a candidate's base resume and a job description, rewrite the resume to:
- Highlight skills and experience that match the job requirements
- Adjust bullet points to use keywords from the job description
- Rewrite the professional summary to target this specific role
- Reorder sections to put the most relevant experience first
- Keep it truthful — enhance presentation, don't fabricate experience
- Keep it to 1-2 pages max
- Use strong action verbs and quantified achievements
- Output in clean, professional plain text format with clear sections"""

COVER_LETTER_SYSTEM_PROMPT = """You are an expert career coach who writes compelling, personalized cover letters.
Given a candidate's resume and a job description, write a cover letter that:
- Is 3-4 paragraphs, under 300 words
- Opens with a strong hook relevant to the specific role
- Connects the candidate's experience to the job requirements
- Shows genuine interest in the company and role
- Closes with a clear call to action
- Sounds natural and human, not templated
- Does NOT use generic phrases like "I am writing to express my interest"
"""


async def tailor_resume(
    resume_text: str,
    job: JobPosting,
) -> dict:
    """Tailor a resume for a specific job posting. Returns tailored resume + cover letter."""
    client = create_llm_client()

    job_info = _build_job_context(job)

    # Generate tailored resume
    resume_message = f"""Here is my base resume:

---
{resume_text}
---

Here is the job I'm applying to:

---
{job_info}
---

Rewrite my resume tailored for this specific job. Output the full resume in clean plain text."""

    tailored_resume = await client.text_message(TAILOR_SYSTEM_PROMPT, resume_message)

    # Generate cover letter
    cover_message = f"""Here is my resume:

---
{resume_text}
---

Here is the job I'm applying to:

---
{job_info}
---

Write a personalized cover letter for this job."""

    cover_letter = await client.text_message(COVER_LETTER_SYSTEM_PROMPT, cover_message)

    usage = client.get_token_usage()

    return {
        "tailored_resume": tailored_resume,
        "cover_letter": cover_letter,
        "provider": detect_provider(),
        "model": client.model,
        "tokens_used": usage["input"] + usage["output"],
    }


def _build_job_context(job: JobPosting) -> str:
    parts = []
    if job.title:
        parts.append(f"Title: {job.title}")
    if job.company:
        parts.append(f"Company: {job.company}")
    if job.location:
        parts.append(f"Location: {job.location}")
    if job.salary_min or job.salary_max:
        salary = ""
        if job.salary_min:
            salary += f"${job.salary_min:,}"
        if job.salary_min and job.salary_max:
            salary += " - "
        if job.salary_max:
            salary += f"${job.salary_max:,}"
        parts.append(f"Salary: {salary}")
    if job.description:
        parts.append(f"\nJob Description:\n{job.description[:3000]}")
    return "\n".join(parts)
