from app.llm.provider import LLMProvider


class OpenAIClient(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o", max_tokens: int = 4096):
        super().__init__(model, max_tokens)
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)

    async def text_message(self, system: str, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_message},
            ],
        )
        if response.usage:
            self.token_usage["input"] += response.usage.prompt_tokens
            self.token_usage["output"] += response.usage.completion_tokens
        return response.choices[0].message.content or ""
