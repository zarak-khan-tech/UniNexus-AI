"""
English: Central registry of all available tools. Agents and the orchestrator
        look up tools by name through this registry.
Roman Urdu: Sab available tools ka central registry. Agents aur orchestrator
        is registry se tools ko naam se dhoondte hain.
"""
import logging
from typing import Dict, List, Optional

from backend.app.tools.base import BaseTool, PermissionLevel

logger = logging.getLogger(__name__)


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """English: Register a tool instance. Overwrites if name exists.
           Roman Urdu: Tool register karo. Agar naam pehle se hai to overwrite."""
        if not tool.name or tool.name == 'base':
            raise ValueError('Tool must define a unique name')
        self._tools[tool.name] = tool
        logger.info(f'Tool registered: {tool.name} ({tool.permission.value})')

    def get(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def list(self, permission: Optional[PermissionLevel] = None) -> List[Dict]:
        """English: List all tools (or filter by permission level).
           Roman Urdu: Sab tools list karo (ya permission level se filter)."""
        tools = list(self._tools.values())
        if permission is not None:
            tools = [t for t in tools if t.permission == permission]
        return [t.to_dict() for t in tools]

    def names(self) -> List[str]:
        return list(self._tools.keys())

    def call(self, name: str, **kwargs) -> 'ToolResult':
        """English: Safely invoke a tool by name. Returns ToolResult.
           Roman Urdu: Tool ko naam se safely call karo. ToolResult return hota hai."""
        from backend.app.tools.base import ToolResult
        tool = self.get(name)
        if not tool:
            return ToolResult(success=False, error=f'Tool not found: {name}')
        try:
            return tool.execute(**kwargs)
        except TypeError as e:
            logger.error(f'Tool {name} bad arguments: {e}')
            return ToolResult(success=False, error=f'Bad arguments: {e}')
        except Exception as e:
            logger.error(f'Tool {name} crashed: {e}')
            return ToolResult(success=False, error=str(e))


# English: Module-level singleton.
# Roman Urdu: Module-level singleton taake pooray app mein ek hi registry rahe.
tool_registry = ToolRegistry()
