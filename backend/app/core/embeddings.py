"""
English: Embedding service that talks to Ollama's embedding endpoint.
Roman Urdu: Embedding service jo Ollama ke embedding endpoint se baat karti hai.
"""
import logging
from typing import List, Optional

import ollama

logger = logging.getLogger(__name__)

DEFAULT_EMBEDDING_MODEL = 'nomic-embed-text'


class EmbeddingService:
    def __init__(self, model: str = DEFAULT_EMBEDDING_MODEL):
        self.model = model

    def embed(self, text: str) -> Optional[List[float]]:
        """
        English: Generate a single embedding vector for a piece of text.
        Roman Urdu: Ek text ke liye single embedding vector generate karo.
        """
        if not text or not text.strip():
            return None
        try:
            response = ollama.embeddings(model=self.model, prompt=text)
            vec = response.get('embedding') if isinstance(response, dict) else getattr(response, 'embedding', None)
            if vec:
                return vec
            logger.warning('Embedding returned empty')
            return None
        except Exception as e:
            logger.error(f'Embedding failed: {e}')
            return None

    def embed_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """
        English: Generate embeddings for a batch of texts.
        Roman Urdu: Kai texts ke liye ek saath embeddings banao.
        """
        return [self.embed(t) for t in texts]


# English: Singleton.
# Roman Urdu: Singleton.
embedding_service = EmbeddingService()
