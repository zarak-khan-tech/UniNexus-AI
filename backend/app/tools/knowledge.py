"""
English: Knowledge/RAG tools. Semantic search over university documents using
         vector embeddings.
Roman Urdu: Knowledge/RAG tools. University documents pe semantic search
            vector embeddings ke zariye.
"""
from backend.app.tools.base import BaseTool, ToolResult, PermissionLevel
from backend.app.core.embeddings import embedding_service
from backend.app.core.vector_store import vector_store

class SemanticSearchTool(BaseTool):
    name = 'semantic_search'
    description = (
        'Semantically search university documents using vector embeddings. '
        'Understands meaning, not just keywords — "break from studies" finds '
        'the Leave of Absence policy. Use this whenever the user asks about '
        'policies, rules, handbooks, fees, hostel, exams, or any university '
        'document.'
    )
    permission = PermissionLevel.READ
    input_schema = {
        'type': 'object',
        'properties': {
            'query': {'type': 'string', 'description': 'Natural language query'},
            'top_k': {'type': 'integer', 'description': 'Number of documents to return (default 3)'},
        },
        'required': ['query'],
    }

    def execute(self, query: str = '', top_k: int = 3, **kwargs) -> ToolResult:
        if not query or not query.strip():
            return ToolResult(success=False, error='query parameter is required')

        # English: Embed the query into a vector.
        # Roman Urdu: Query ko vector mein embed karo.
        vec = embedding_service.embed(query)
        if not vec:
            return ToolResult(success=False, error='Failed to embed query')

        # English: Search the vector store for top-k similar documents.
        # Roman Urdu: Vector store mein top-k milte-julte documents dhoondo.
        results = vector_store.search(vec, top_k=top_k)

        # English: Shape output for the frontend (keeps existing UI working).
        # Roman Urdu: Output shape frontend ke liye (existing UI kaam kare).
        docs = []
        for r in results:
            content = r.get('content', '') or ''
            docs.append({
                'id': r.get('id'),
                'title': r.get('title'),
                'category': r.get('category'),
                'content_preview': (content[:320] + '…') if len(content) > 320 else content,
                'similarity': r.get('similarity'),
            })

        return ToolResult(
            success=True,
            data=docs,
            metadata={'count': len(docs), 'query': query, 'engine': 'semantic_vector_search'},
        )
