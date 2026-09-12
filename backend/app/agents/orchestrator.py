from backend.app.agents.base import BaseAgent
from backend.app.agents.registry import registry
from typing import Dict, Any

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Orchestrator",
            description="Central intelligence layer responsible for planning and delegating tasks."
        )

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        user_request = task.get("request", "").lower()
        
        # 1. Plan
        plan = []
        if "attendance" in user_request:
            plan = [
                {"step": 1, "agent": "AttendanceAgent", "action": "Fetch low-attendance data"},
                {"step": 2, "agent": "PolicyAgent", "action": "Check attendance threshold policy"},
                {"step": 3, "agent": "RiskAgent", "action": "Analyze academic risk"}
            ]
        elif "risk" in user_request:
            plan = [
                {"step": 1, "agent": "RiskAgent", "action": "Identify at-risk students"}
            ]
        else:
            plan = [
                {"step": 1, "agent": "AttendanceAgent", "action": "Fetch generic data"}
            ]
        
        # 2. Execute
        execution_log = []
        for step in plan:
            agent_name = step["agent"]
            agent = registry.get_agent(agent_name)
            
            if agent:
                result = agent.execute(task)
                execution_log.append({
                    "step": step["step"],
                    "agent": agent_name,
                    "action": step["action"],
                    "result": result
                })
            else:
                execution_log.append({
                    "step": step["step"],
                    "agent": agent_name,
                    "action": step["action"],
                    "error": "Agent not found in registry."
                })

        return {
            "status": "completed",
            "orchestrator": self.name,
            "original_request": user_request,
            "execution_plan": plan,
            "execution_results": execution_log
        }
