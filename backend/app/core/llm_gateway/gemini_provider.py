"""
English: Gemini provider — wraps Google's google-genai SDK.
Roman Urdu: Gemini provider — Google ke google-genai SDK ko wrap karta hai.
"""
import os
import logging
from typing import Dict, Any, Optional

from backend.app.core.llm_gateway.base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)

# English: Try importing google.genai. If unavailable, mark it gracefully.
# Roman Urdu: Google genai import karne ki koshish. Agar na ho, gracefully mark karo.
try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class GeminiProvider(LLMProvider):
    name = "gemini"

    def __init__(self, model: str = None, api_key: str = None):
        # English: Read model + key from env, with sensible defaults.
        # Roman Urdu: Model aur key env se parho, sensible defaults ke saath.
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-flash-latest")
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._client = None

    @property
    def client(self):
        # English: Lazily construct the client only when needed.
        # Roman Urdu: Client sirf tab banao jab zaroorat ho.
        if self._client is None and self.api_key and GENAI_AVAILABLE:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

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

        # English: Build config — force JSON output if requested.
        # Roman Urdu: Config banao — agar JSON chahiye to mime type set karo.
        config = None
        if json_mode:
            config = {"response_mime_type": "application/json"}

        # English: Try the primary model, then fall back to alternate models.
        # Roman Urdu: Pehle primary model, agar fail ho to alternate models try karo.
        models_to_try = [self.model, "gemini-flash-latest", "gemini-2.5-flash"]
        last_error: Optional[str] = None

        for m in models_to_try:
            try:
                response = self.client.models.generate_content(
                    model=m, contents=prompt, config=config
                )
                text = getattr(response, "text", "") or ""
                return LLMResponse(
                    text=text, provider=self.name, model=m, success=True
                )
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Gemini model {m} failed: {last_error[:160]}")

        return LLMResponse(
            text="", provider=self.name, model=self.model,
            success=False, error=last_error or "All Gemini models failed"
        )

    def status(self) -> Dict[str, Any]:
        return {
            "available": bool(self.api_key and GENAI_AVAILABLE),
            "model": self.model,
            "has_api_key": bool(self.api_key),
        }
