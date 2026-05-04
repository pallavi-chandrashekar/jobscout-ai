from app.models.models import JobPosting
from app.schemas.schemas import OutreachGenerateResponse
from app.llm.factory import create_llm_client, detect_provider
from app.llm.prompts import get_system_prompt, build_outreach_user_message


async def generate_outreach_message(
    job: JobPosting,
    outreach_type: str,
    tone: str,
    resume_summary: str | None,
) -> OutreachGenerateResponse:
    client = create_llm_client()
    system_prompt = get_system_prompt(outreach_type)
    user_message = build_outreach_user_message(
        job_title=job.title,
        company=job.company,
        description=job.description,
        resume_summary=resume_summary,
        tone=tone,
    )

    message = await client.text_message(system_prompt, user_message)
    usage = client.get_token_usage()

    return OutreachGenerateResponse(
        message=message,
        provider=detect_provider(),
        model=client.model,
        tokens_used=usage["input"] + usage["output"],
    )
