"""
English: Verify KnowledgeAgent now uses semantic search via the tool registry.
Roman Urdu: Verify karo ke KnowledgeAgent ab semantic search use kar raha hai 
tool registry ke zariye.
"""
from backend.app.agents.registry import registry
from backend.app.agents.specialized import AttendanceAgent, PolicyAgent, RiskAgent, KnowledgeAgent

# Register agents
registry.register(AttendanceAgent())
registry.register(PolicyAgent())
registry.register(RiskAgent())
registry.register(KnowledgeAgent())

print('=' * 60)
print('Testing KnowledgeAgent with semantic queries')
print('=' * 60)

agent = registry.get_agent('KnowledgeAgent')

queries = [
    'what happens if I fail an exam',
    'how much does semester cost',
    'I want to take a break from studies',
]

for q in queries:
    print()
    print('-' * 60)
    print('QUERY:', q)
    print('-' * 60)
    result = agent.execute({'request': q})
    print('Tool used:', result.get('tool_used'))
    print('Matches:', result.get('total_matches'))
    for doc in result.get('documents', []):
        print(f"  [{doc.get('similarity')}] {doc.get('title')} ({doc.get('category')})")
        print(f"    {doc.get('content_preview', '')[:100]}...")
