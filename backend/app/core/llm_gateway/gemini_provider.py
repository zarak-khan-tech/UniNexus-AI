"""
English: Gemini provider — tries the smallest, fastest model first to avoid 503 latency.
Roman Urdu: Gemini provider — sabse chhota, fast model pehle try karta hai taake 503 ki latency se bacha jaye.
"""
import os
import time
import logging
from typing import Dict, Any, Optional

from backend.app.core.llm_gateway.base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class GeminiProvider(LLMProvider):
    name = "gemini"

    # English: Fast/available models first. Bigger models can wait as fallbacks.
    # Roman Urdu: Fast/available models pehle. Bade models fallback ke taur pe baad mein.
    FALLBACK_MODELS = [
        "gemini-flash-lite-latest",
        "gemini-flash-latest",
        "gemini-3.8-flash",
        "gemini-3.5-flash",
    ]

    def __init__(self, model: str = None, api_key: str = None):
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._client = None

    @property
    def client(self):
        if self._client is None and self.api_key and GENAI_AVAILABLE:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def _try_model(self, model_name: str, prompt: str, config):
        """
        English: Send one request to one model. Returns (text, error_str).
        Roman Urdu: Ek model ko ek request bhejo. (text, error_str) return karta hai.
        """
        try:
            response = self.client.models.generate_content(
                model=model_name, contents=prompt, config=config
            )
            return (getattr(response, "text", "") or ""), None
        except Exception as e:
            return None, str(e)

    def generate(self, prompt: str, json_mode: bool = False) -> LLMResponse:
        if not GENAI_AVAILABLE:
            return LLMResponse(
                text="", provider=self.name, model=self.model,
                success=False, error="google-genai package not installed"
            )
        if not self.api_key:
            return LLMResponse(
                text="", provider=self.name, model=self.model,
                success=False, error="GEMINI_API_KEY not set"
            )

        config = {"response_mime_type": "application/json"} if json_mode else None

        # English: Build a de-duplicated model list — the current default first, then fallbacks.
        # Roman Urdu: Duplicate-free model list banao — default pehle, phir fallbacks.
        models = [self.model]
        for m in self.FALLBACK_MODELS:
            if m not in models:
                models.append(m)

        # English: Collect failures so we can report a useful error if all fail.
        # Roman Urdu: Failures jama karo taake agar sab fail hon to clear error mile.
        failures = []

        for model_name in models:
            text, err = self._try_model(model_name, prompt, config)

            if text:
                logger.info(f"Gemini success via {model_name}")
                return LLMResponse(
                    text=text, provider=self.name, model=model_name, success=True
                )

            # English: 503 = temporary. Move on quickly, don't waste time retrying.
            # Roman Urdu: 503 = temporary. Jaldi agle model pe jao, retry mein time zaya na karo.
            failures.append(f"{model_name}: {(err or '')[:80]}")
            logger.warning(f"Gemini {model_name} failed: {(err or '')[:80]}")

        # English: If EVERY model returned 503, wait briefly and try the first one once more.
        # Roman Urdu: Agar sab models 503 de rahe hain to thora ruk ke pehla model ek baar phir try karo.
        if all("503" in f for f in failures):
            logger.info("All models 503 — waiting 3s and retrying the first once...")
            time.sleep(3)
            text, err = self._try_model(models[0], prompt, config)
            if text:
                return LLMResponse(
                    text=text, provider=self.name, model=models[0], success=True
                )
            failures.append(f"retry-{models[0]}: {(err or '')[:80]}")

        return LLMResponse(
            text="", provider=self.name, model=self.model,
            success=False, error=" | ".join(failures) or "All Gemini models failed"
        )

    def status(self) -> Dict[str, Any]:
        return {
            "available": bool(self.api_key and GENAI_AVAILABLE),
            "model": self.model,
            "has_api_key": bool(self.api_key),
            "fallback_models": self.FALLBACK_MODELS,
        }
