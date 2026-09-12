from backend.app.agents.base import BaseAgent
from backend.app.agents.registry import registry
from backend.app.core.llm import plan_with_llm
from typing import Dict, Any

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name='Orchestrator',
            description='Central intelligence layer responsible for planning and delegating tasks.'
        )

    def _fallback_plan(self, user_request: str):
        if 'attendance' in user_request:
            return [
                {'step': 1, 'agent': 'AttendanceAgent', 'action': 'Fetch low-attendance data'},
                {'step': 2, 'agent': 'PolicyAgent', 'action': 'Check attendance threshold policy'},
                {'step': 3, 'agent': 'RiskAgent', 'action': 'Analyze academic risk'},
            ]
        if 'risk' in user_request:
            return [
                {'step': 1, 'agent': 'RiskAgent', 'action': 'Identify at-risk students'},
            ]
        return [
            {'step': 1, 'agent': 'KnowledgeAgent', 'action': 'Search university documents'},
        ]

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        user_request = task.get('request', '').lower()
        available_agents = [a['name'] for a in registry.list_agents()]

        plan = plan_with_llm(user_request, available_agents)
        planning_source = 'llm'
        if not plan:
            plan = self._fallback_plan(user_request)
            planning_source = 'fallback'

        execution_log = []
        for step in plan:
            agent_name = step['agent']
            agent = registry.get_agent(agent_name)
            if agent:
                try:
                    result = agent.execute(task)
                    execution_log.append({
                        'step': step['step'],
                        'agent': agent_name,
                        'action': step['action'],
                        'result': result,
                    })
                except Exception as e:
                    execution_log.append({
                        'step': step['step'],
                        'agent': agent_name,
                        'action': step['action'],
                        'error': f'Agent execution failed: {str(e)}',
                    })
            else:
                execution_log.append({
                    'step': step['step'],
                    'agent': agent_name,
                    'action': step['action'],
                    'error': 'Agent not found in registry.',
                })

        return {
            'status': 'completed',
            'orchestrator': self.name,
            'original_request': user_request,
            'planning_source': planning_source,
            'execution_plan': plan,
            'execution_results': execution_log,
        }
