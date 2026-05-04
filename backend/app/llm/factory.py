import importlib

from app.config import get_settings
from app.llm.provider import LLMProvider

PROVIDER_CONFIG = {
    "claude": {
        "env_key": "anthropic_api_key",
        "default_model": "claude-sonnet-4-5-20250929",
        "module": "app.llm.claude_client",
        "class_name": "ClaudeClient",
    },
    "openai": {
        "env_key": "openai_api_key",
        "default_model": "gpt-4o",
        "module": "app.llm.openai_client",
        "class_name": "OpenAIClient",
    },
    "gemini": {
        "env_key": "google_api_key",
        "default_model": "gemini-2.0-flash",
        "module": "app.llm.gemini_client",
        "class_name": "GeminiClient",
    },
    "ollama": {
        "env_key": None,
        "default_model": "llama3.1",
        "module": "app.llm.ollama_client",
        "class_name": "OllamaClient",
    },
}


def detect_provider() -> str:
    settings = get_settings()
    if settings.llm_provider:
        return settings.llm_provider
    if settings.anthropic_api_key:
        return "claude"
    if settings.openai_api_key:
        return "openai"
    if settings.google_api_key:
        return "gemini"
    return "ollama"


def create_llm_client(provider: str | None = None) -> LLMProvider:
    provider = provider or detect_provider()
    config = PROVIDER_CONFIG.get(provider)
    if not config:
        raise ValueError(f"Unknown LLM provider: {provider}. Supported: {list(PROVIDER_CONFIG.keys())}")

    settings = get_settings()
    model = settings.llm_model or config["default_model"]

    mod = importlib.import_module(config["module"])
    client_class = getattr(mod, config["class_name"])

    if config["env_key"]:
        api_key = getattr(settings, config["env_key"], None)
        if not api_key:
            raise ValueError(f"{config['env_key'].upper()} is required for '{provider}' provider")
        return client_class(api_key=api_key, model=model)
    else:
        return client_class(model=model, base_url=settings.ollama_base_url)
