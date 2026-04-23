"""
Similarity scoring and ranking engine
"""
from app.schemas import StartupMatch
from collections import Counter
import logging

logger = logging.getLogger(__name__)


def compute_uniqueness_score(similarity_scores: list) -> tuple:
    """
    Compute uniqueness score (0-100) based on top similarity scores.
    Higher score = more unique idea.
    """
    if not similarity_scores:
        return 100.0, "Highly Unique"

    # Use average of top 3 similarities
    top_scores = sorted(similarity_scores, reverse=True)[:3]
    avg_top_similarity = sum(top_scores) / len(top_scores)

    # Uniqueness = inverse of similarity
    uniqueness = (1 - avg_top_similarity) * 100
    uniqueness = max(0, min(100, uniqueness))  # Clamp to 0-100

    # Label
    if uniqueness >= 70:
        label = "Highly Unique"
    elif uniqueness >= 40:
        label = "Moderately Unique"
    else:
        label = "Crowded Space"

    return round(uniqueness, 1), label


def process_search_results(results: dict) -> list:
    """
    Process raw ChromaDB results into ranked StartupMatch objects.
    ChromaDB returns cosine distances (0 = identical, 2 = opposite).
    We convert to similarity: similarity = 1 - (distance / 2)
    """
    matches = []

    if not results or not results.get("ids") or not results["ids"][0]:
        return matches

    ids = results["ids"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]
    documents = results["documents"][0]

    for i, (doc_id, distance, metadata, document) in enumerate(
        zip(ids, distances, metadatas, documents)
    ):
        # Convert cosine distance to similarity score (0-1)
        # ChromaDB cosine distance ranges from 0 (identical) to 2 (opposite)
        similarity = 1 - (distance / 2)
        similarity = max(0, min(1, similarity))  # Clamp

        # Parse tags from metadata
        tags_str = metadata.get("tags", "")
        tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else []

        match = StartupMatch(
            name=metadata.get("name", "Unknown"),
            description=metadata.get("description", document),
            category=metadata.get("category", "Other"),
            tags=tags,
            founded_year=metadata.get("founded_year"),
            funding_stage=metadata.get("funding_stage"),
            status=metadata.get("status"),
            url=metadata.get("url"),
            similarity_score=round(similarity, 4),
            similarity_percentage=round(similarity * 100, 1)
        )
        matches.append(match)

    # Sort by similarity (highest first)
    matches.sort(key=lambda m: m.similarity_score, reverse=True)

    return matches


def get_category_distribution(matches: list) -> dict:
    """Get distribution of categories in the matched results"""
    categories = [m.category for m in matches if m.category]
    return dict(Counter(categories))
