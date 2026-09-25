"""
English: Groq provider — uses Groq's free tier for fast inference of open models.
Roman Urdu: Groq provider — Groq ke free tier ko use karta hai tez inference ke liye.
"""
import os
import logging
from typing import Dict, Any, Optional

from backend.app.core.llm_gateway.base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class GroqProvider(LLMProvider):
    name = "groq"

    # English: Preferred model — gpt-oss-120b is the strongest available on Groq today.
    # Roman Urdu: Preferred model — gpt-oss-120b aaj Groq pe sab se strong hai.
    DEFAULT_MODEL = "openai/gpt-oss-120b"
    FALLBACK_MODELS = [
        "openai/gpt-oss-120b",
        "qwen/qwen3.8-27b",
        "openai/gpt-oss-20b",
        "allam-2-7b",
    ]

    def __init__(self, model: str = None, api_key: str = None):
        self.model = model or os.getenv("GROQ_MODEL", self.DEFAULT_MODEL)
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self._client = None

    @property
    def client(self):
        if self._client is None and self.api_key and GROQ_AVAILABLE:
            self._client = Groq(api_key=self.api_key)
        return self._client

    def generate(self, prompt: str, json_mode: bool = False) -> LLMResponse:
        if not GROQ_AVAILABLE:
            return LLMResponse(
                text="", provider=self.name, model=self.model,
                success=False, error="groq package not installed"
            )
        if not self.api_key:
            return LLMResponse(
                text="", provider=self.name, model=self.model,
                success=False, error="GROQ_API_KEY not set"
            )

        models = [self.model] + [m for m in self.FALLBACK_MODELS if m != self.model]
        last_error: Optional[str] = None

        for model_name in models:
            try:
                kwargs = {
                    "model": model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                }
                if json_mode:
                    kwargs["response_format"] = {"type": "json_object"}

                completion = self.client.chat.completions.create(**kwargs)
                text = completion.choices[0].message.content or ""
                if text:
                    logger.info(f"Groq success via {model_name}")
                    return LLMResponse(
                        text=text, provider=self.name, model=model_name, success=True
                    )
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Groq {model_name} failed: {last_error[:120]}")

        return LLMResponse(
            text="", provider=self.name, model=self.model,
            success=False, error=last_error or "All Groq models failed"
        )

    def status(self) -> Dict[str, Any]:
        return {
            "available": bool(self.api_key and GROQ_AVAILABLE),
            "model": self.model,
            "has_api_key": bool(self.api_key),
            "fallback_models": self.FALLBACK_MODELS,
        }
