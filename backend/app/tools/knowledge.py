"""
English: Knowledge/RAG tools. Semantic search over university documents with 
relevance filtering — strong/weak/none evidence classification.
Roman Urdu: Knowledge/RAG tools. University documents pe semantic search, 
relevance filtering ke saath.
"""
from backend.app.tools.base import BaseTool, ToolResult, PermissionLevel
from backend.app.core.embeddings import embedding_service
from backend.app.core.vector_store import vector_store


# English: Evidence-quality thresholds for RAG grounding.
# Roman Urdu: RAG grounding ke liye evidence-quality thresholds.
STRONG_EVIDENCE_THRESHOLD = 0.65   # Solid match — quote confidently
WEAK_EVIDENCE_THRESHOLD = 0.45     # Related — answer with caveat
# Below WEAK_EVIDENCE_THRESHOLD → no useful evidence


class SemanticSearchTool(BaseTool):
    name = 'semantic_search'
    description = (
        'Semantically search university documents using vector embeddings. '
        'Returns matched documents with an evidence_quality marker '
        '(strong/weak/none) so the reasoning core knows how confidently '
        'to answer. Use this whenever the user asks about policies, rules, '
        'handbooks, fees, hostel, exams, or any university document.'
    )
    permission = PermissionLevel.READ
    input_schema = {
        'type': 'object',
        'properties': {
            'query': {'type': 'string', 'description': 'Natural language query'},
            'top_k': {'type': 'integer', 'description': 'Number of documents to return (default 3, max 5)'},
        },
        'required': ['query'],
    }

    def execute(self, query: str = '', top_k: int = 3, **kwargs) -> ToolResult:
        if not query or not query.strip():
            return ToolResult(success=False, error='query parameter is required')

        vec = embedding_service.embed(query)
        if not vec:
            return ToolResult(success=False, error='Failed to embed query')

        raw_results = vector_store.search(vec, top_k=min(top_k, 5))

        # English: Classify each match by similarity; drop anything below weak.
        # Roman Urdu: Har match ko similarity se classify karo; weak se neeche
        # wale drop karo.
        docs = []
        best_similarity = 0.0
        for r in raw_results:
            content = r.get('content', '') or ''
            sim = r.get('similarity') or 0.0
            if sim > best_similarity:
                best_similarity = sim
            if sim < WEAK_EVIDENCE_THRESHOLD:
                continue  # not useful
            quality = 'strong' if sim >= STRONG_EVIDENCE_THRESHOLD else 'weak'
            docs.append({
                'id': r.get('id'),
                'title': r.get('title'),
                'category': r.get('category'),
                'content': content,
                'similarity': sim,
                'evidence_quality': quality,
            })

        # English: Overall evidence quality for this retrieval.
        # Roman Urdu: Iss retrieval ka overall evidence quality.
        if not docs:
            overall = 'none'
        elif any(d['evidence_quality'] == 'strong' for d in docs):
            overall = 'strong'
        else:
            overall = 'weak'

        return ToolResult(
            success=True,
            data=docs,
            metadata={
                'count': len(docs),
                'query': query,
                'engine': 'semantic_vector_search',
                'evidence_quality': overall,
                'best_similarity': round(best_similarity, 4),
                'thresholds': {
                    'strong': STRONG_EVIDENCE_THRESHOLD,
                    'weak': WEAK_EVIDENCE_THRESHOLD,
                },
            },
        )
