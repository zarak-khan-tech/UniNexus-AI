"""
English: Ollama provider — wraps the local Ollama Python client.
Roman Urdu: Ollama provider — local Ollama Python client ko wrap karta hai.
"""
import os
import logging
from typing import Dict, Any

from backend.app.core.llm_gateway.base import LLMProvider, LLMResponse

logger = logging.getLogger(__name__)

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class OllamaProvider(LLMProvider):
    name = "ollama"

    def __init__(self, model: str = None):
        # English: Default to the smaller 1B model to reduce RAM pressure on 8GB machines.
        # Roman Urdu: Default chhota 1B model rakha hai taake 8GB machines pe RAM pressure kam ho.
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2:1b")

    def generate(self, prompt: str, json_mode: bool = False) -> LLMResponse:
        if not OLLAMA_AVAILABLE:
            return LLMResponse(
                text="", provider=self.name, model=self.model,
                success=False, error="ollama python package not installed"
            )
        try:
            kwargs = {
                "model": self.model,
                "prompt": prompt,
                "keep_alive": "5m",
                "options": {"temperature": 0.1},
            }
            if json_mode:
                kwargs["format"] = "json"

            response = ollama.generate(**kwargs)
            text = response.get("response", "") if isinstance(response, dict) else getattr(response, "response", "")
            return LLMResponse(
                text=text or "", provider=self.name, model=self.model, success=True
            )
        except Exception as e:
            logger.error(f"Ollama generate failed: {e}")
            return LLMResponse(
                text="", provider=self.name, model=self.model,
                success=False, error=str(e)
            )

    def status(self) -> Dict[str, Any]:
        if not OLLAMA_AVAILABLE:
            return {
                "available": False,
                "model": self.model,
                "reason": "ollama python package not installed",
            }
        try:
            listing = ollama.list()
            raw = listing.get("models", []) if isinstance(listing, dict) else getattr(listing, "models", [])
            names = []
            for m in raw:
                n = m.get("name") if isinstance(m, dict) else getattr(m, "model", None)
                if n:
                    names.append(n)
            model_ready = any(self.model in (n or "") for n in names)
            return {
                "available": True,
                "model": self.model,
                "model_ready": model_ready,
                "installed_models": names,
            }
        except Exception as e:
            return {"available": False, "model": self.model, "reason": str(e)}
