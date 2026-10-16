# English: Add GET /agents/health — per-agent execution stats.
# Roman Urdu: GET /agents/health add karo — per-agent execution stats.
path = "backend/app/api/agents.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

addition = '''

@router.get('/health')
def agents_health(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    English: Return per-agent stats — execution count, last-used timestamp, 
    and success rate.
    Roman Urdu: Per-agent stats return karo — execution count, last used 
    timestamp, aur success rate.
    """
    from collections import defaultdict

    executions = db.query(AgentExecution).filter(
        AgentExecution.tenant_id == current_user.tenant_id,
    ).order_by(AgentExecution.created_at.desc()).limit(500).all()

    stats = defaultdict(lambda: {'runs': 0, 'last_used': None, 'success': 0, 'failure': 0})

    for ex in executions:
        try:
            plan = json.loads(ex.execution_plan_json or '[]')
        except Exception:
            plan = []
        try:
            results = json.loads(ex.execution_results_json or '[]')
        except Exception:
            results = []

        # English: Map each step to its result status.
        # Roman Urdu: Har step ko uske result status se map karo.
        result_by_step = {}
        if isinstance(results, list):
            for r in results:
                if isinstance(r, dict) and 'step' in r:
                    result_by_step[r['step']] = r

        for step in (plan if isinstance(plan, list) else []):
            if not isinstance(step, dict):
                continue
            agent_name = step.get('agent')
            if not agent_name:
                continue
            s = stats[agent_name]
            s['runs'] += 1
            if not s['last_used'] or ex.created_at > s['last_used']:
                s['last_used'] = ex.created_at
            result = result_by_step.get(step.get('step'), {})
            if result.get('error'):
                s['failure'] += 1
            else:
                s['success'] += 1

    out = []
    for name, s in stats.items():
        total = s['success'] + s['failure']
        rate = round(100.0 * s['success'] / total, 1) if total else 100.0
        out.append({
            'agent': name,
            'runs': s['runs'],
            'success': s['success'],
            'failure': s['failure'],
            'success_rate': rate,
            'last_used': s['last_used'].isoformat() if s['last_used'] else None,
        })

    out.sort(key=lambda x: x['runs'], reverse=True)
    return {'total': len(out), 'agents': out}
'''

if 'def agents_health' in content:
    print("SKIP: health endpoint already present")
else:
    content = content.rstrip() + addition + '\n'
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: /agents/health endpoint added")
