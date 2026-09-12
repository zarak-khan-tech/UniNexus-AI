from typing import Dict
from backend.app.agents.base import BaseAgent

class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent):
        self._agents[agent.name] = agent

    def get_agent(self, name: str) -> BaseAgent:
        return self._agents.get(name)

    def list_agents(self):
        return [{"name": a.name, "description": a.description} for a in self._agents.values()]

# Global registry instance
registry = AgentRegistry()
