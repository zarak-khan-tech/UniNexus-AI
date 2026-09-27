"""
English: Knowledge/RAG tools. Semantic search over university documents.
Roman Urdu: Knowledge/RAG tools. University documents pe semantic search.
"""
from backend.app.tools.base import BaseTool, ToolResult, PermissionLevel
from backend.app.core.embeddings import embedding_service
from backend.app.core.vector_store import vector_store

class SemanticSearchTool(BaseTool):
    name = 'semantic_search'
    description = (
        'Semantically search university documents using vector embeddings. '
        'Returns FULL document text so you can quote accurately. '
        'Use this whenever the user asks about policies, rules, handbooks, '
        'fees, hostel, exams, or any university document.'
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

        results = vector_store.search(vec, top_k=min(top_k, 5))

        # English: Return FULL content (not just preview) so the LLM can
        #          quote accurately and NOT hallucinate.
        # Roman Urdu: Poora content return karo (preview nahi) taake LLM
        #             sahi quote kare aur hallucinate na kare.
        docs = []
        for r in results:
            content = r.get('content', '') or ''
            docs.append({
                'id': r.get('id'),
                'title': r.get('title'),
                'category': r.get('category'),
                'content': content,  # FULL content — no truncation
                'similarity': r.get('similarity'),
            })

        return ToolResult(
            success=True,
            data=docs,
            metadata={'count': len(docs), 'query': query, 'engine': 'semantic_vector_search'},
        )
