"""
English: Foundation for the tool system. Every tool inherits from BaseTool,
        has a permission level, and returns a structured ToolResult.
Roman Urdu: Tool system ki bunyad. Har tool BaseTool se inherit karta hai,
        ek permission level rakhta hai, aur structured ToolResult return karta hai.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional


class PermissionLevel(str, Enum):
    """
    English: Risk classification for tool actions.
             READ = safe read-only.
             WRITE_LOW = reversible, low-impact writes (drafts, notifications).
             WRITE_HIGH = sensitive actions requiring human approval (grades, records).
    Roman Urdu: Har tool ki action ka risk level.
             READ = safe sirf parhna.
             WRITE_LOW = reversible, chhote writes (drafts, notifications).
             WRITE_HIGH = sensitive actions jinke liye human approval chahiye (grades, records).
    """
    READ = 'read'
    WRITE_LOW = 'write_low'
    WRITE_HIGH = 'write_high'


@dataclass
class ToolResult:
    """
    English: Standard result shape every tool returns.
    Roman Urdu: Har tool isi shape mein result return karta hai.
    """
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseTool(ABC):
    """
    English: Abstract base class. Every tool must define:
             - name: unique snake_case identifier
             - description: short explanation for LLM planning
             - permission: one of PermissionLevel
             - input_schema: JSON-Schema-like description of parameters
             - execute(**kwargs) -> ToolResult
    Roman Urdu: Abstract base class. Har tool ko define karna hoga:
             - name: unique snake_case naam
             - description: chhoti si explanation LLM planning ke liye
             - permission: PermissionLevel mein se ek
             - input_schema: parameters ka JSON-Schema jaisa description
             - execute(**kwargs) -> ToolResult
    """
    name: str = 'base'
    description: str = ''
    permission: PermissionLevel = PermissionLevel.READ
    input_schema: Dict[str, Any] = {}

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        """Serializable description used for LLM planning and API responses."""
        return {
            'name': self.name,
            'description': self.description,
            'permission': self.permission.value,
            'input_schema': self.input_schema,
        }
