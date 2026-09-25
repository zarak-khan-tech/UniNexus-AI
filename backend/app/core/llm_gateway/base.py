"""
English: Base interface that every LLM provider must implement.
Roman Urdu: Har LLM provider ko ye interface implement karna hoga.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class LLMResponse:
    """
    English: Standard response shape returned by every provider.
    Roman Urdu: Har provider isi shape mein response return karega.
    """
    text: str
    provider: str
    model: str
    success: bool
    error: Optional[str] = None


class LLMProvider(ABC):
    """
    English: Abstract base for LLM providers. Providers implement `generate` and `status`.
    Roman Urdu: LLM providers ka abstract base. Har provider `generate` aur `status` banata hai.
    """
    name: str = "base"

    @abstractmethod
    def generate(self, prompt: str, json_mode: bool = False) -> LLMResponse:
        """
        English: Generate a completion. If json_mode is True, ask the model for JSON output.
        Roman Urdu: Completion generate karo. Agar json_mode True ho to model se JSON output maango.
        """
        raise NotImplementedError

    @abstractmethod
    def status(self) -> Dict[str, Any]:
        """
        English: Return a status dictionary (availability, model name, etc.).
        Roman Urdu: Status dictionary return karo (availability, model name, waghera).
        """
        raise NotImplementedError
