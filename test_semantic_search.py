from backend.app.core.embeddings import embedding_service
from backend.app.core.vector_store import vector_store

# English: Test with a query that does NOT literally contain the document words.
# Roman Urdu: Aisi query se test karo jismein literally document ke alfaz na hon.
queries = [
    'test rules and exam conduct',
    'money and payment obligations',
    'student dormitory guidelines',
    'plagiarism and cheating',
]

for q in queries:
    print()
    print('=' * 60)
    print('QUERY:', q)
    print('=' * 60)
    vec = embedding_service.embed(q)
    results = vector_store.search(vec, top_k=3)
    for r in results:
        print(f"  [{r['similarity']}] {r['title']} ({r['category']})")
