from backend.app.agents.base import BaseAgent
from typing import Dict, Any

class AttendanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="AttendanceAgent", description="Analyzes student attendance data.")
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # Mock data retrieval
        return {
            "status": "success",
            "agent": self.name,
            "data": [
                {"student_id": 101, "name": "Ali Khan", "attendance_percentage": 65},
                {"student_id": 102, "name": "Sara Ahmed", "attendance_percentage": 58}
            ]
        }

class PolicyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="PolicyAgent", description="Checks institutional policies and thresholds.")
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # Mock policy check
        return {
            "status": "success",
            "agent": self.name,
            "policy_threshold": 75,
            "rule": "Students below 75% attendance require intervention."
        }

class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="RiskAgent", description="Analyzes academic risk based on data and policy.")
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # Mock risk analysis
        return {
            "status": "success",
            "agent": self.name,
            "at_risk_students": [
                {"student_id": 101, "risk_level": "Medium"},
                {"student_id": 102, "risk_level": "High"}
            ]
        }
