"""
English: Verify RAG relevance filtering with strong/weak/none evidence.
Roman Urdu: RAG relevance filtering test karo — strong/weak/none evidence.
"""
from backend.app.core.database import SessionLocal
from backend.app.models.tenant import Tenant
from backend.app.core.reasoning import reason

db = SessionLocal()
t = db.query(Tenant).first()
tid = t.id
db.close()

tests = [
    ("what happens if I fail an exam?", "expected: STRONG evidence"),
    ("what is the cafeteria food quality rating?", "expected: WEAK or NONE"),
    ("what is the wifi password for the dean's office?", "expected: NONE"),
]

for query, note in tests:
    print("=" * 70)
    print(f"QUERY: {query}")
    print(f"({note})")
    print("=" * 70)
    r = reason(query, user_id=1, user_email="admin@demo.university.edu", tenant_id=tid)

    # Show evidence quality metadata from semantic_search tool calls
    for tc in r.get('tool_calls', []):
        if tc['tool'] == 'semantic_search':
            summary = tc.get('summary', {})
            print(f"  semantic_search: {summary.get('count', 0)} results")

    print(f"Sources: {[s['title'] for s in r.get('sources', [])]}")
    print(f"Answer preview: {r.get('answer', '')[:250]}...")
    print()
