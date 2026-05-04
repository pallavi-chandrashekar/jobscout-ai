from abc import ABC, abstractmethod


class LLMProvider(ABC):
    def __init__(self, model: str, max_tokens: int = 4096):
        self.model = model
        self.max_tokens = max_tokens
        self.token_usage = {"input": 0, "output": 0}

    @abstractmethod
    async def text_message(self, system: str, user_message: str) -> str:
        """Send a message and get text response."""

    def get_token_usage(self) -> dict:
        return {**self.token_usage}
