"""
English: Document ingestion pipeline — chunk text, embed each chunk, and 
store in the Document table + vector store.
Roman Urdu: Document ingestion pipeline — text ko chunk karo, har chunk ko 
embed karo, aur Document table + vector store mein store karo.
"""
import logging
from typing import Dict, Any, List
from backend.app.core.database import SessionLocal
from backend.app.core.embeddings import embedding_service
from backend.app.core.vector_store import vector_store
from backend.app.models.document import Document
from backend.app.core.events import event_bus, Event

logger = logging.getLogger(__name__)

# English: Chunking parameters.
# Roman Urdu: Chunking ke parameters.
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    English: Simple paragraph-aware chunking. Split by double newlines first,
    then group paragraphs until chunk_size. Add small overlap between chunks.
    Roman Urdu: Simple paragraph-aware chunking. Pehle double newlines pe 
    split karo, phir paragraphs ko group karo chunk_size tak. Chunks ke 
    darmiyan chhota overlap add karo.
    """
    text = (text or '').strip()
    if not text:
        return []
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks: List[str] = []
    current = ''
    for p in paragraphs:
        if len(current) + len(p) + 2 <= chunk_size:
            current = (current + '\n\n' + p).strip() if current else p
        else:
            if current:
                chunks.append(current)
            # English: If a single paragraph is huge, hard-split it.
            # Roman Urdu: Agar ek paragraph bahut bara ho, hard-split karo.
            if len(p) > chunk_size:
                for i in range(0, len(p), chunk_size - overlap):
                    chunks.append(p[i:i + chunk_size])
                current = ''
            else:
                current = p
    if current:
        chunks.append(current)
    return chunks


def ingest_document(tenant_id: int, title: str, category: str, content: str) -> Dict[str, Any]:
    """
    English: Persist a Document row and embed its chunks into the vector 
    store. Returns summary.
    Roman Urdu: Document row save karo aur iske chunks ko vector store mein 
    embed karo. Summary return karo.
    """
    db = SessionLocal()
    try:
        doc = Document(
            tenant_id=tenant_id,
            title=title,
            category=category or 'Policy',
            content=content,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        doc_id = doc.id
    finally:
        db.close()

    chunks = chunk_text(content)
    embedded = 0
    for i, chunk in enumerate(chunks):
        vec = embedding_service.embed(f"{title}\n\n{chunk}")
        if not vec:
            logger.warning(f"Failed to embed chunk {i} of doc {doc_id}")
            continue
        vector_store.add(vec, {
            'id': doc_id,
            'title': title,
            'category': category or 'Policy',
            'content': chunk,  # full chunk, so semantic_search can quote it
            'tenant_id': tenant_id,
            'chunk_index': i,
        })
        embedded += 1

    vector_store.save()
    # English: Publish an event so subscribers (workflows, notifications) can react.
    # Roman Urdu: Event publish karo taake subscribers (workflows, notifications) react kar sakein.
    try:
        event_bus.publish(Event(
            event_type='DocumentUploaded',
            tenant_id=tenant_id,
            payload={
                'document_id': doc_id,
                'title': title,
                'category': category or 'Policy',
                'chunks': embedded,
            },
        ))
    except Exception as e:
        logger.warning(f"Failed to publish DocumentUploaded event: {e}")

    return {
        'document_id': doc_id,
        'title': title,
        'category': category or 'Policy',
        'total_chunks': len(chunks),
        'embedded_chunks': embedded,
    }
