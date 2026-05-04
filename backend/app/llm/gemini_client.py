from app.llm.provider import LLMProvider


class GeminiClient(LLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", max_tokens: int = 4096):
        super().__init__(model, max_tokens)
        from google.generativeai import GenerativeModel, configure
        configure(api_key=api_key)
        self._model = GenerativeModel(model)

    async def text_message(self, system: str, user_message: str) -> str:
        prompt = f"System: {system}\n\nUser: {user_message}"
        response = self._model.generate_content(
            prompt,
            generation_config={"max_output_tokens": self.max_tokens},
        )
        usage = getattr(response, "usage_metadata", None)
        if usage:
            self.token_usage["input"] += getattr(usage, "prompt_token_count", 0)
            self.token_usage["output"] += getattr(usage, "candidates_token_count", 0)
        return response.text
