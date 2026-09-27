from backend.app.core.embeddings import embedding_service
from backend.app.core.vector_store import vector_store

# English: Test with semantic (not literal) queries.
# Roman Urdu: Semantic (literal nahi) queries se test karo.
queries = [
    'what happens if I fail an exam',
    'how much does semester cost',
    'I want to take a break from studies',
    'can I stay in the dorm over summer',
    'what if my CGPA drops too low',
]

for q in queries:
    print()
    print('=' * 60)
    print('QUERY:', q)
    print('=' * 60)
    vec = embedding_service.embed(q)
    results = vector_store.search(vec, top_k=3)
    for r in results:
        preview = r['content'][:120].replace('\n', ' ')
        print(f"  [{r['similarity']}] {r['title']}")
        print(f"      {preview}...")
