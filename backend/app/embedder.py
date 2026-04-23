"""
Embedding pipeline using HuggingFace Inference API (Free, Lightweight, No PyTorch)
"""
import requests
import re
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class Embedder:
    """Handles text embedding using HuggingFace API to save memory on Render"""

    def __init__(self):
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/{settings.embedding_model}"
        self.headers = {"Authorization": f"Bearer {settings.huggingface_api_key}"}

    def load_model(self):
        """Nothing to load locally since we use an API!"""
        logger.info(f"Using HuggingFace API for embeddings: {settings.embedding_model}")

    def preprocess(self, text: str) -> str:
        """Clean and preprocess text before embedding"""
        text = text.lower().strip()
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'[^\w\s.,!?-]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:2000]

    def embed(self, text: str) -> list:
        """Generate embedding for a single text"""
        processed = self.preprocess(text)
        return self._call_api([processed])[0]

    def embed_batch(self, texts: list) -> list:
        """Generate embeddings for multiple texts"""
        processed = [self.preprocess(t) for t in texts]
        
        # HuggingFace API can handle batches, but we chunk to avoid payload limits
        chunk_size = 10
        all_embeddings = []
        
        for i in range(0, len(processed), chunk_size):
            chunk = processed[i:i + chunk_size]
            embeddings = self._call_api(chunk)
            all_embeddings.extend(embeddings)
            
        return all_embeddings

    def _call_api(self, texts: list) -> list:
        """Make request to HuggingFace"""
        try:
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                json={"inputs": texts, "options": {"wait_for_model": True}}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"HuggingFace API Error: {e}")
            # Return dummy zero embeddings on failure to prevent crash
            return [[0.0] * 384 for _ in texts]

    def enrich_startup_text(self, name: str, description: str, category: str, tags: list) -> str:
        """Combine startup fields into a richer text for better embeddings"""
        parts = []
        if name: parts.append(f"{name}.")
        if category: parts.append(f"Category: {category}.")
        if description: parts.append(description)
        if tags: parts.append(f"Tags: {', '.join(tags)}.")
        return " ".join(parts)


# Singleton instance
embedder = Embedder()
