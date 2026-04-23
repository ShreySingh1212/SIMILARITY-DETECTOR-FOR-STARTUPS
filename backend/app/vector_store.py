"""
Lightweight in-memory vector store using NumPy (replaces ChromaDB)
This avoids C++ compiler requirements on Windows for Python 3.13.
"""
import numpy as np
import json
import os
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages NumPy arrays for vector similarity search"""

    def __init__(self):
        self.db_path = settings.chroma_db_path + "_numpy.json"
        self.data = {
            "ids": [],
            "embeddings": [],
            "documents": [],
            "metadatas": []
        }

    def initialize(self):
        """Load data from disk if it exists"""
        if os.path.exists(self.db_path):
            logger.info(f"Loading vector store from {self.db_path}")
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                logger.info(f"Loaded {len(self.data['ids'])} startups.")
            except Exception as e:
                logger.error(f"Failed to load vector store: {e}")
                self.reset()
        else:
            logger.info("Initializing new empty vector store.")

    def save(self):
        """Save data to disk"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f)

    def add_startups(self, ids: list, embeddings: list, documents: list, metadatas: list):
        """Batch add startups to the vector store"""
        # Append new data
        self.data["ids"].extend(ids)
        self.data["embeddings"].extend(embeddings)
        self.data["documents"].extend(documents)
        self.data["metadatas"].extend(metadatas)
        
        # Save to disk
        self.save()
        logger.info(f"Added {len(ids)} startups. Total: {self.get_count()}")

    def search_similar(self, query_embedding: list, top_k: int = 10) -> dict:
        """Search for similar startups given a query embedding"""
        if self.get_count() == 0:
            return {"ids": [[]], "distances": [[]], "documents": [[]], "metadatas": [[]]}

        # Convert to numpy arrays
        q_vec = np.array(query_embedding)
        db_vecs = np.array(self.data["embeddings"])

        # Compute cosine similarities
        # sim = dot(A, B) / (norm(A) * norm(B))
        q_norm = np.linalg.norm(q_vec)
        db_norms = np.linalg.norm(db_vecs, axis=1)
        
        # Handle zero norms
        if q_norm == 0:
            similarities = np.zeros(len(db_vecs))
        else:
            with np.errstate(divide='ignore', invalid='ignore'):
                similarities = np.dot(db_vecs, q_vec) / (db_norms * q_norm)
                similarities = np.nan_to_num(similarities, 0)

        # ChromaDB distance = 1 - cosine_similarity (range 0 to 2)
        distances = 1 - similarities

        # Get top_k indices
        top_k = min(top_k, self.get_count())
        top_indices = np.argsort(distances)[:top_k]

        # Format exactly like ChromaDB output
        return {
            "ids": [[self.data["ids"][i] for i in top_indices]],
            "distances": [[float(distances[i]) for i in top_indices]],
            "documents": [[self.data["documents"][i] for i in top_indices]],
            "metadatas": [[self.data["metadatas"][i] for i in top_indices]]
        }

    def get_count(self) -> int:
        """Get total number of startups in the vector store"""
        return len(self.data["ids"])

    def is_seeded(self) -> bool:
        """Check if the database has been seeded"""
        return self.get_count() > 0

    def reset(self):
        """Clear all data (for re-seeding)"""
        self.data = {
            "ids": [],
            "embeddings": [],
            "documents": [],
            "metadatas": []
        }
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        logger.info("Vector store reset.")


# Singleton instance
vector_store = VectorStore()
