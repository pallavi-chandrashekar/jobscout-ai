from app.llm.provider import LLMProvider


class ClaudeClient(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929", max_tokens: int = 4096):
        super().__init__(model, max_tokens)
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)

    async def text_message(self, system: str, user_message: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system,
            messages=[{"role": "user", "content": user_message}],
        )
        if response.usage:
            self.token_usage["input"] += response.usage.input_tokens
            self.token_usage["output"] += response.usage.output_tokens
        return response.content[0].text
