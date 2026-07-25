import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


class Settings:
    PROJECT_NAME: str = "AIMap Backend Core"
    VERSION: str = "1.0.0"

    # OpenRouter API settings
    OPENROUTER_API_URL: str = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

    # Default Small Models (1B - 3B parameter range)
    SMALL_MODELS: List[str] = [
        "meta-llama/llama-3.2-1b-instruct",
        "qwen/qwen-2.5-1.5b-instruct",
        "google/gemma-2-2b-it",
        "deepseek/deepseek-r1-distill-qwen-1.5b",
    ]
    DEFAULT_MODEL: str = "meta-llama/llama-3.2-1b-instruct"

    # Fallback Mock Settings
    # Auto-enable mock mode if API key is not provided or if AIMAP_MOCK_MODE=true
    @property
    def MOCK_MODE(self) -> bool:
        forced_mock = os.getenv("AIMAP_MOCK_MODE", "").lower() in ("true", "1", "yes")
        has_key = bool(self.OPENROUTER_API_KEY and self.OPENROUTER_API_KEY.strip())
        return forced_mock or not has_key

    # Standard headers for OpenRouter
    @property
    def OPENROUTER_HEADERS(self) -> dict:
        return {
            "Authorization": f"Bearer {self.OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://aimap.ai",
            "X-Title": "AIMap AI Interview Platform",
            "Content-Type": "application/json",
        }


settings = Settings()
