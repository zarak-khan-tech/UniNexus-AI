"""
English: Orchestrator — plans tasks and delegates to agents. Respects
         tenant-configured active agents (disabled agents are skipped).
Roman Urdu: Orchestrator — tasks plan karta hai aur agents ko delegate karta hai.
            Tenant ke active agents respect karta hai (disabled skip hote hain).
"""
import logging
from typing import Dict, Any, List
from backend.app.agents.base import BaseAgent
from backend.app.agents.registry import registry
from backend.app.core.llm import plan_with_llm

logger = logging.getLogger(__name__)


class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name='Orchestrator',
            description='Central intelligence layer responsible for planning and delegating tasks.',
        )

    def _get_active_agent_names(self, tenant_id):
        """English: Active agent names from DB for this tenant. Falls back to
        class-level list if DB is empty (e.g. before migration).
        Roman Urdu: Tenant ke active agent names DB se. Agar DB khali ho to
        class-level list fallback."""
        if tenant_id:
            try:
                return [a['name'] for a in registry.list_agents_for_tenant(tenant_id)]
            except Exception as e:
                logger.warning(f'Failed to read tenant agent defs: {e}')
        return [a['name'] for a in registry.list_agents()]

    def _fallback_plan(self, user_request: str, active_names: List[str]) -> List[Dict]:
        """English: Deterministic fallback plan, filtered to only include
        currently active agents.
        Roman Urdu: Deterministic fallback plan, sirf active agents include karta hai."""
        def keep(plan):
            return [s for s in plan if s['agent'] in active_names]

        if 'attendance' in user_request:
            return keep([
                {'step': 1, 'agent': 'AttendanceAgent', 'action': 'Fetch low-attendance data'},
                {'step': 2, 'agent': 'PolicyAgent', 'action': 'Check attendance threshold policy'},
                {'step': 3, 'agent': 'RiskAgent', 'action': 'Analyze academic risk'},
            ])
        if 'risk' in user_request:
            return keep([
                {'step': 1, 'agent': 'RiskAgent', 'action': 'Identify at-risk students'},
            ])
        return keep([
            {'step': 1, 'agent': 'KnowledgeAgent', 'action': 'Search university documents'},
        ])

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        user_request = task.get('request', '').lower()
        tenant_id = task.get('tenant_id')

        # English: Get tenant's active agents for planning.
        # Roman Urdu: Tenant ke active agents plan ke liye nikalo.
        active_names = self._get_active_agent_names(tenant_id)
        if not active_names:
            return {
                'status': 'error',
                'orchestrator': self.name,
                'original_request': user_request,
                'error': 'No active agents configured for this tenant.',
                'execution_plan': [],
                'execution_results': [],
            }

        parsed = plan_with_llm(user_request, active_names)
        planning_source = 'llm'

        if not parsed:
            plan = self._fallback_plan(user_request, active_names)
            if not plan:
                return {
                    'status': 'error',
                    'orchestrator': self.name,
                    'original_request': user_request,
                    'error': 'Fallback plan produced no viable agent steps.',
                    'execution_plan': [],
                    'execution_results': [],
                }
            parsed = {'mode': 'agent_workflow', 'plan': plan, 'answer': ''}
            planning_source = 'fallback'

        # English: Handle direct_answer from LLM (casual query).
        # Roman Urdu: LLM se direct_answer handle karo (casual query).
        if parsed['mode'] == 'direct_answer':
            return {
                'status': 'completed',
                'orchestrator': self.name,
                'original_request': user_request,
                'planning_source': planning_source,
                'mode': 'direct_answer',
                'direct_answer': parsed['answer'],
                'execution_plan': [],
                'execution_results': [],
            }

        # English: Double-check every agent in the plan is still active.
        # Roman Urdu: Plan mein har agent active ho ye dobara check karo.
        plan = parsed['plan']
        execution_log = []
        for step in plan:
            agent_name = step['agent']
            if agent_name not in active_names:
                execution_log.append({
                    'step': step['step'], 'agent': agent_name,
                    'action': step['action'],
                    'error': 'Agent is disabled for this tenant.',
                })
                continue

            agent = registry.get_agent(agent_name)
            if not agent:
                execution_log.append({
                    'step': step['step'], 'agent': agent_name,
                    'action': step['action'],
                    'error': 'Agent not found in registry.',
                })
                continue

            try:
                result = agent.execute(task)
                execution_log.append({
                    'step': step['step'], 'agent': agent_name,
                    'action': step['action'], 'result': result,
                })
            except Exception as e:
                execution_log.append({
                    'step': step['step'], 'agent': agent_name,
                    'action': step['action'],
                    'error': f'Agent execution failed: {str(e)}',
                })

        return {
            'status': 'completed',
            'orchestrator': self.name,
            'original_request': user_request,
            'planning_source': planning_source,
            'mode': 'agent_workflow',
            'direct_answer': '',
            'execution_plan': plan,
            'execution_results': execution_log,
        }
