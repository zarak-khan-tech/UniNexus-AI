"""
English: Lightweight persistent vector store using numpy + pickle.
        Chosen over FAISS/Chroma to keep installs small on the user's machine.
Roman Urdu: Halka persistent vector store, numpy + pickle pe based.
        FAISS/Chroma ke bajaye ye chuna taake user ki machine pe install halka rahe.
"""
import os
import pickle
import logging
from typing import List, Dict, Any, Optional

import numpy as np

logger = logging.getLogger(__name__)

STORE_PATH = '.vector_store.pkl'


class VectorStore:
    def __init__(self, path: str = STORE_PATH):
        self.path = path
        self.vectors: Optional[np.ndarray] = None
        self.documents: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        """English: Load from disk if the store file exists.
           Roman Urdu: Agar store file disk pe hai to load karo."""
        if os.path.exists(self.path):
            try:
                with open(self.path, 'rb') as f:
                    data = pickle.load(f)
                    self.vectors = data.get('vectors')
                    self.documents = data.get('documents', [])
                logger.info(f'Vector store loaded: {len(self.documents)} docs')
            except Exception as e:
                logger.error(f'Failed to load vector store: {e}')

    def _save(self):
        """English: Persist to disk.
           Roman Urdu: Disk pe save karo."""
        try:
            with open(self.path, 'wb') as f:
                pickle.dump({'vectors': self.vectors, 'documents': self.documents}, f)
        except Exception as e:
            logger.error(f'Failed to save vector store: {e}')

    def add(self, embedding: List[float], metadata: Dict[str, Any]) -> None:
        """
        English: Add a single (vector, metadata) pair. Vector is L2-normalized
                 so cosine similarity becomes a simple dot product.
        Roman Urdu: Ek (vector, metadata) pair add karo. Vector L2-normalize
                 kiya jata hai taake cosine similarity simple dot product ban jaye.
        """
        if not embedding:
            return
        vec = np.array(embedding, dtype=np.float32)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm

        if self.vectors is None:
            self.vectors = vec.reshape(1, -1)
        else:
            if vec.shape[0] != self.vectors.shape[1]:
                logger.error(f'Embedding dimension mismatch: {vec.shape[0]} vs {self.vectors.shape[1]}')
                return
            self.vectors = np.vstack([self.vectors, vec.reshape(1, -1)])

        self.documents.append(metadata)

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """
        English: Return top-k most similar documents via cosine similarity.
        Roman Urdu: Top-k sab se milte-julte documents cosine similarity se return karo.
        """
        if self.vectors is None or self.vectors.size == 0 or not query_embedding:
            return []

        q = np.array(query_embedding, dtype=np.float32)
        norm = np.linalg.norm(q)
        if norm > 0:
            q = q / norm

        if q.shape[0] != self.vectors.shape[1]:
            logger.error('Query embedding dimension mismatch')
            return []

        sims = self.vectors @ q  # cosine similarity (both normalized)
        top_idx = np.argsort(sims)[::-1][:top_k]

        results = []
        for i in top_idx:
            doc = dict(self.documents[int(i)])
            doc['similarity'] = round(float(sims[int(i)]), 4)
            results.append(doc)
        return results

    def clear(self) -> None:
        """English: Wipe the store.
           Roman Urdu: Store saaf karo."""
        self.vectors = None
        self.documents = []
        if os.path.exists(self.path):
            os.remove(self.path)

    def count(self) -> int:
        return len(self.documents)

    def save(self) -> None:
        """Public save — call after bulk adds."""
        self._save()


# English: Singleton.
# Roman Urdu: Singleton.
vector_store = VectorStore()
