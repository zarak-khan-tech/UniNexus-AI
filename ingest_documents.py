"""
English: One-time script to embed all documents in the DB into the vector store.
        Safe to re-run — clears and rebuilds.
Roman Urdu: Ek dafa chalane wali script jo DB ke sab documents ko vector store mein embed karti hai.
        Dobara chalana safe hai — clear karke rebuild karti hai.
"""
from backend.app.core.database import SessionLocal
from backend.app.core.embeddings import embedding_service
from backend.app.core.vector_store import vector_store
from backend.app.models.document import Document


def main():
    print('Clearing old vector store...')
    vector_store.clear()

    db = SessionLocal()
    try:
        docs = db.query(Document).all()
        print(f'Found {len(docs)} documents to embed')

        for i, doc in enumerate(docs, 1):
            # English: Embed title + content together for better retrieval.
            # Roman Urdu: Better retrieval ke liye title + content mila ke embed karo.
            text = f'{doc.title}\n\n{doc.content}'
            vec = embedding_service.embed(text)
            if not vec:
                print(f'  [{i}/{len(docs)}] FAILED: {doc.title}')
                continue

            vector_store.add(vec, {
                'id': doc.id,
                'title': doc.title,
                'category': doc.category,
                'content': doc.content,
                'tenant_id': doc.tenant_id,
            })
            print(f'  [{i}/{len(docs)}] embedded: {doc.title}')

        vector_store.save()
        print(f'\nDone. Vector store contains {vector_store.count()} documents.')
    finally:
        db.close()


if __name__ == '__main__':
    main()
