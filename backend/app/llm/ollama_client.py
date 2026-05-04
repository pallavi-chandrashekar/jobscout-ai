import httpx

from app.llm.provider import LLMProvider


class OllamaClient(LLMProvider):
    def __init__(self, model: str = "llama3.1", max_tokens: int = 4096, base_url: str = "http://localhost:11434"):
        super().__init__(model, max_tokens)
        self.base_url = base_url

    async def text_message(self, system: str, user_message: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user_message},
                    ],
                    "stream": False,
                    "options": {"num_predict": self.max_tokens},
                },
                timeout=120.0,
            )
            response.raise_for_status()
            data = response.json()
            if data.get("prompt_eval_count") or data.get("eval_count"):
                self.token_usage["input"] += data.get("prompt_eval_count", 0)
                self.token_usage["output"] += data.get("eval_count", 0)
            return data.get("message", {}).get("content", "")
