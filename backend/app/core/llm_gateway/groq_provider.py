"""
English: Groq provider — uses Groq's free tier for fast inference of open models.
Roman Urdu: Groq provider — Groq ke free tier ko use karta hai tez inference ke liye.
"""
import os
import json
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

    # English: Preferred model (fast + smart). Fallback if unavailable.
    # Roman Urdu: Preferred model (tez + smart). Agar na ho to fallback.
    DEFAULT_MODEL = "llama-3.3-70b-versatile"
    FALLBACK_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
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

        # English: Try each model in order; return first successful response.
        # Roman Urdu: Har model ko order mein try karo; pehla successful return karo.
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
