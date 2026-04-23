"""
Embedding pipeline using sentence-transformers (local, free, no API key)
"""
from sentence_transformers import SentenceTransformer
from app.config import settings
import re
import logging

logger = logging.getLogger(__name__)


class Embedder:
    """Handles text embedding using sentence-transformers"""

    def __init__(self):
        self.model = None

    def load_model(self):
        """Load the embedding model (called once at startup)"""
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        self.model = SentenceTransformer(settings.embedding_model)
        logger.info("Embedding model loaded successfully")

    def preprocess(self, text: str) -> str:
        """Clean and preprocess text before embedding"""
        # Lowercase
        text = text.lower().strip()
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        # Remove special characters but keep meaningful punctuation
        text = re.sub(r'[^\w\s.,!?-]', ' ', text)
        # Collapse multiple spaces
        text = re.sub(r'\s+', ' ', text).strip()
        # Truncate to reasonable length
        return text[:2000]

    def embed(self, text: str) -> list:
        """Generate embedding for a single text"""
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        processed = self.preprocess(text)
        embedding = self.model.encode(processed)
        return embedding.tolist()

    def embed_batch(self, texts: list) -> list:
        """Generate embeddings for multiple texts efficiently"""
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        processed = [self.preprocess(t) for t in texts]
        embeddings = self.model.encode(processed, batch_size=32, show_progress_bar=True)
        return embeddings.tolist()

    def enrich_startup_text(self, name: str, description: str, category: str, tags: list) -> str:
        """Combine startup fields into a richer text for better embeddings"""
        parts = []
        if name:
            parts.append(f"{name}.")
        if category:
            parts.append(f"Category: {category}.")
        if description:
            parts.append(description)
        if tags:
            parts.append(f"Tags: {', '.join(tags)}.")
        return " ".join(parts)


# Singleton instance
embedder = Embedder()
