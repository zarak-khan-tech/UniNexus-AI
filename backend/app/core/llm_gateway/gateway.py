"""
English: LLM Gateway — unified interface with runtime provider switching.
Roman Urdu: LLM Gateway — runtime provider switching ke saath unified interface.
"""
import os
import logging
from typing import Optional, Dict

from dotenv import load_dotenv
load_dotenv()

from backend.app.core.llm_gateway.base import LLMResponse
from backend.app.core.llm_gateway.ollama_provider import OllamaProvider
from backend.app.core.llm_gateway.gemini_provider import GeminiProvider
from backend.app.core.llm_gateway.groq_provider import GroqProvider

logger = logging.getLogger(__name__)


class LLMGateway:
    """
    English: Manages providers, allows runtime switching, saves choice to .env.
    Roman Urdu: Providers manage karta hai, runtime switching allow karta hai, choice .env mein save karta hai.
    """

    def __init__(self):
        self.primary_name = os.getenv("LLM_PROVIDER", "groq").lower().strip()

        self.providers = {
            "groq": GroqProvider(),
            "gemini": GeminiProvider(),
            "ollama": OllamaProvider(),
        }

    def list_providers(self):
        """
        English: Return all providers with their status — used by frontend dropdown.
        Roman Urdu: Sab providers ka status return karo — frontend dropdown ke liye.
        """
        out = []
        for name, p in self.providers.items():
            st = p.status()
            out.append({
                "name": name,
                "model": st.get("model"),
                "available": st.get("available", False),
                "is_primary": name == self.primary_name,
                "details": st,
            })
        return out

    def set_primary(self, name: str) -> bool:
        """
        English: Switch primary provider at runtime AND persist to .env.
        Roman Urdu: Primary provider runtime pe switch karo AUR .env mein save karo.
        """
        name = (name or "").lower().strip()
        if name not in self.providers:
            return False

        self.primary_name = name
        self._persist_to_env("LLM_PROVIDER", name)
        logger.info(f"LLM provider switched to {name}")
        return True

    @staticmethod
    def _persist_to_env(key: str, value: str):
        # English: Upsert into .env so choice survives backend restart.
        # Roman Urdu: .env mein update karo taake backend restart pe choice bachi rahe.
        env_path = ".env"
        lines = []
        found = False
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f.read().splitlines():
                    if line.startswith(f"{key}="):
                        lines.append(f"{key}={value}")
                        found = True
                    else:
                        lines.append(line)
        if not found:
            lines.append(f"{key}={value}")
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    def _order(self):
        order = [self.primary_name]
        for name in self.providers:
            if name != self.primary_name:
                order.append(name)
        return order

    def generate(self, prompt: str, json_mode: bool = False) -> LLMResponse:
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
        primary = self.providers.get(self.primary_name)
        primary_status = primary.status() if primary else {"available": False}
        return {
            "primary_provider": self.primary_name,
            "primary_available": primary_status.get("available", False),
            "primary_model": primary_status.get("model"),
            "primary_status": primary_status,
            "providers": self.list_providers(),
        }


_gateway: Optional[LLMGateway] = None


def get_gateway() -> LLMGateway:
    global _gateway
    if _gateway is None:
        _gateway = LLMGateway()
    return _gateway
