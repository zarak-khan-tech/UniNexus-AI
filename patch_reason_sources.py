# English: Patch the /reason endpoint response to include sources.
# Roman Urdu: /reason endpoint ke response mein sources field add karo.
path = "backend/app/api/agents.py"
with open(path, "r", encoding="utf-8-sig") as f:
    content = f.read()

old = """    return {
        'mode': 'agentic_reasoning',
        'original_request': task_req.request,
        'answer': result.get('answer'),
        'tool_calls': result.get('tool_calls', []),
        'iterations': result.get('iterations', 0),
        'provider': result.get('provider'),
        'model': result.get('model'),
        'execution_id': execution.id,
        'duration_ms': round(duration_ms, 2),
        'status': 'completed' if not result.get('error') else 'partial',
    }"""

new = """    return {
        'mode': 'agentic_reasoning',
        'original_request': task_req.request,
        'answer': result.get('answer'),
        'tool_calls': result.get('tool_calls', []),
        'iterations': result.get('iterations', 0),
        'provider': result.get('provider'),
        'model': result.get('model'),
        'execution_id': execution.id,
        'duration_ms': round(duration_ms, 2),
        'status': 'completed' if not result.get('error') else 'partial',
        # English: Deduped RAG sources for the frontend.
        # Roman Urdu: Frontend ke liye deduped RAG sources.
        'sources': result.get('sources', []),
    }"""

if old not in content:
    print("ERROR: /reason return block not found")
    raise SystemExit(1)

content = content.replace(old, new, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("OK: /reason now returns sources")
