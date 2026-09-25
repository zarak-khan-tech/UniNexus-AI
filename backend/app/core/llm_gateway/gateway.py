"""
English: LLM Gateway — unified interface with primary + fallback providers.
Roman Urdu: LLM Gateway — ek unified interface jahan primary aur fallback providers hain.
"""
import os
import logging
from typing import Optional

# English: Load .env into os.environ so os.getenv() works in providers.
# Roman Urdu: .env ko os.environ mein load karo taake providers ka os.getenv() kaam kare.
from dotenv import load_dotenv
load_dotenv()

from backend.app.core.llm_gateway.base import LLMResponse
from backend.app.core.llm_gateway.ollama_provider import OllamaProvider
from backend.app.core.llm_gateway.gemini_provider import GeminiProvider

logger = logging.getLogger(__name__)


class LLMGateway:
    """
    English: Picks a primary provider from .env, with automatic fallback.
    Roman Urdu: .env se primary provider chunta hai, aur automatically fallback karta hai.
    """

    def __init__(self):
        # English: Which provider to try first — controlled via .env LLM_PROVIDER.
        # Roman Urdu: Pehle konsa provider try karna hai — .env mein LLM_PROVIDER se control.
        self.primary_name = os.getenv("LLM_PROVIDER", "gemini").lower().strip()

        self.providers = {
            "gemini": GeminiProvider(),
            "ollama": OllamaProvider(),
        }

    def _order(self):
        """
        English: Primary first, then all others as fallbacks.
        Roman Urdu: Pehle primary, phir baaki sab fallback ke taur pe.
        """
        order = [self.primary_name]
        for name in self.providers:
            if name != self.primary_name:
                order.append(name)
        return order

    def generate(self, prompt: str, json_mode: bool = False) -> LLMResponse:
        """
        English: Try each provider in order; return the first successful response.
        Roman Urdu: Har provider ko order mein try karo; pehla successful response return karo.
        """
        errors = []
        for name in self._order():
            provider = self.providers.get(name)
            if not provider:
                continue
            resp = provider.generate(prompt, json_mode=json_mode)
            if resp.success:
                logger.info(f"LLM gateway: used {name} ({resp.model})")
                return resp
            errors.append(f"{name}: {resp.error}")
            logger.warning(f"LLM gateway: {name} failed, trying next...")

        return LLMResponse(
            text="", provider="none", model="none",
            success=False, error=" | ".join(errors),
        )

    def status(self):
        """
        English: Return a rich status for the /agents/llm/status endpoint.
        Roman Urdu: /agents/llm/status endpoint ke liye ek rich status return karo.
        """
        primary = self.providers.get(self.primary_name)
        primary_status = primary.status() if primary else {"available": False}

        fallbacks = {}
        for name, p in self.providers.items():
            if name != self.primary_name:
                fallbacks[name] = p.status()

        return {
            "primary_provider": self.primary_name,
            "primary_available": primary_status.get("available", False),
            "primary_model": primary_status.get("model"),
            "primary_status": primary_status,
            "fallback_providers": fallbacks,
            "ollama_status": self.providers["ollama"].status(),
        }


_gateway: Optional[LLMGateway] = None


def get_gateway() -> LLMGateway:
    global _gateway
    if _gateway is None:
        _gateway = LLMGateway()
    return _gateway
