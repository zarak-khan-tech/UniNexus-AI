"""
English: Central agent registry — classes in memory, metadata in DB.
Roman Urdu: Central agent registry — classes memory mein, metadata DB mein.
"""
import logging
from typing import Dict, List, Optional
from backend.app.tools.base import PermissionLevel
from backend.app.tools.registry import tool_registry  # noqa (kept for compatibility)

logger = logging.getLogger(__name__)


class AgentRegistry:
    """English: Holds agent class instances (for execution) and reads
    metadata from the DB (for listing).
    Roman Urdu: Agent class instances rakhta hai (execution ke liye) aur
    metadata DB se padhta hai (listing ke liye)."""

    def __init__(self):
        self._agents: Dict[str, 'BaseAgent'] = {}

    def register(self, agent) -> None:
        if not agent.name or agent.name == 'base':
            raise ValueError('Agent must define a unique name')
        self._agents[agent.name] = agent
        logger.info(f'Agent registered: {agent.name}')

    def get_agent(self, name: str):
        return self._agents.get(name)

    def names(self) -> List[str]:
        return list(self._agents.keys())

    def list_agents(self) -> List[Dict]:
        """English: Class-level fallback — used when no tenant context is available.
        Roman Urdu: Class-level fallback — jab tenant context na ho."""
        return [
            {'name': a.name, 'description': a.description}
            for a in self._agents.values()
        ]

    def list_agents_for_tenant(self, tenant_id: int) -> List[Dict]:
        """English: Read agent metadata from DB for a tenant. Falls back to
        class list if DB has nothing (e.g. before migration ran).
        Roman Urdu: Tenant ke liye agent metadata DB se padho. Agar DB khali
        ho to class list fallback karo."""
        from backend.app.services.agent_definitions import list_agent_definitions
        db_rows = list_agent_definitions(tenant_id, active_only=True)
        if db_rows:
            return db_rows
        return self.list_agents()

    def list(self, permission: Optional['PermissionLevel'] = None) -> List[Dict]:
        """English: List registered tools (kept here for convenience).
        Roman Urdu: Registered tools list karo."""
        return tool_registry.list(permission)


# English: Module-level singleton.
# Roman Urdu: Module-level singleton.
registry = AgentRegistry()
