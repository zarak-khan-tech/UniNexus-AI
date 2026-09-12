from backend.app.agents.base import BaseAgent
from typing import Dict, Any

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Orchestrator",
            description="Central intelligence layer responsible for planning and delegating tasks."
        )

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        user_request = task.get("request", "").lower()
        
        # Mock planning logic (will be replaced with LLM reasoning later)
        plan = []
        if "attendance" in user_request:
            plan = [
                {"step": 1, "agent": "AttendanceAgent", "action": "Fetch low-attendance data"},
                {"step": 2, "agent": "PolicyAgent", "action": "Check attendance threshold policy"},
                {"step": 3, "agent": "RiskAgent", "action": "Analyze academic risk"},
                {"step": 4, "agent": "NotificationAgent", "action": "Draft warning notification"}
            ]
        elif "risk" in user_request:
            plan = [
                {"step": 1, "agent": "AnalyticsAgent", "action": "Analyze student grades"},
                {"step": 2, "agent": "RiskAgent", "action": "Identify at-risk students"},
                {"step": 3, "agent": "RecommendationAgent", "action": "Generate intervention plan"}
            ]
        else:
            plan = [
                {"step": 1, "agent": "KnowledgeAgent", "action": "Search university documents"}
            ]
            
        return {
            "status": "planned",
            "orchestrator": self.name,
            "original_request": user_request,
            "execution_plan": plan
        }
