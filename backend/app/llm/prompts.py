def build_cover_letter_system_prompt() -> str:
    return """You are an expert career coach who writes compelling, personalized cover letters.
Write a cover letter that:
- Is concise (3-4 paragraphs, under 300 words)
- Opens with a strong hook relevant to the role
- Highlights specific skills matching the job requirements
- Shows genuine interest in the company
- Closes with a clear call to action
- Does NOT use generic filler phrases like "I am writing to express my interest"
- Matches the requested tone"""


def build_recruiter_message_system_prompt() -> str:
    return """You are an expert at writing concise, effective recruiter outreach messages.
Write a message that:
- Is brief (2-3 paragraphs, under 150 words)
- Mentions the specific role
- Highlights 1-2 relevant qualifications
- Requests a conversation, not a job
- Sounds natural and human, not templated
- Matches the requested tone"""


def build_follow_up_system_prompt() -> str:
    return """You are an expert at writing professional follow-up messages after job applications.
Write a follow-up message that:
- Is brief (2 paragraphs, under 100 words)
- References the role applied for
- Reiterates interest without being pushy
- Adds one new piece of value (recent achievement, relevant insight)
- Matches the requested tone"""


def get_system_prompt(outreach_type: str) -> str:
    prompts = {
        "cover_letter": build_cover_letter_system_prompt,
        "recruiter_message": build_recruiter_message_system_prompt,
        "follow_up": build_follow_up_system_prompt,
    }
    builder = prompts.get(outreach_type, build_cover_letter_system_prompt)
    return builder()


def build_outreach_user_message(
    job_title: str | None,
    company: str | None,
    description: str | None,
    resume_summary: str | None,
    tone: str,
) -> str:
    parts = [f"Tone: {tone}"]
    if job_title:
        parts.append(f"Role: {job_title}")
    if company:
        parts.append(f"Company: {company}")
    if description:
        parts.append(f"Job Description:\n{description[:2000]}")
    if resume_summary:
        parts.append(f"My Background:\n{resume_summary[:1000]}")
    return "\n\n".join(parts)
