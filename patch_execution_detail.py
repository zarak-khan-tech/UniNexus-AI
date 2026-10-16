# English: Add GET /agents/executions/{id} — returns full execution detail.
# Roman Urdu: GET /agents/executions/{id} add karo — full execution detail 
# return kare.
path = "backend/app/api/agents.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Anchor: append at end of file (after last endpoint).
addition = '''

@router.get('/executions/{execution_id}')
def get_execution_detail(
    execution_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    English: Return full detail for a single execution (plan, results, 
    duration, sources, safety).
    Roman Urdu: Ek single execution ki poori detail return karo (plan, 
    results, duration, sources, safety).
    """
    row = db.query(AgentExecution).filter(
        AgentExecution.id == execution_id,
        AgentExecution.tenant_id == current_user.tenant_id,
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail='Execution not found')

    try:
        plan = json.loads(row.execution_plan_json or '[]')
    except Exception:
        plan = []
    try:
        results = json.loads(row.execution_results_json or '[]')
    except Exception:
        results = {}

    return {
        'id': row.id,
        'tenant_id': row.tenant_id,
        'user_email': row.user_email,
        'original_request': row.original_request,
        'status': row.status,
        'duration_ms': row.duration_ms,
        'created_at': row.created_at.isoformat(),
        'execution_plan': plan,
        'execution_results': results,
    }
'''

# Only add if not already present
if 'def get_execution_detail' in content:
    print("SKIP: detail endpoint already present")
else:
    content = content.rstrip() + addition + '\n'
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK: /agents/executions/{id} endpoint added")
