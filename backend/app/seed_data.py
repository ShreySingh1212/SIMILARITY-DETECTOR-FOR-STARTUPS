"""
Seed data loader - reads startups.json and populates ChromaDB
"""
import json
import os
import logging

logger = logging.getLogger(__name__)

SEED_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "startups.json")


def load_seed_data() -> list:
    """Load startup data from JSON file"""
    if not os.path.exists(SEED_FILE):
        logger.error(f"Seed file not found: {SEED_FILE}")
        return []
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info(f"Loaded {len(data)} startups from seed file")
    return data


def seed_vector_store(embedder, vector_store):
    """Embed and store all seed startups into ChromaDB"""
    if vector_store.is_seeded():
        logger.info(f"Vector store already seeded with {vector_store.get_count()} startups. Skipping.")
        return

    startups = load_seed_data()
    if not startups:
        logger.warning("No seed data to load.")
        return

    logger.info(f"Seeding {len(startups)} startups into vector store...")

    ids = []
    texts = []
    metadatas = []

    for i, s in enumerate(startups):
        startup_id = f"startup_{i}_{s['name'].lower().replace(' ', '_')}"
        enriched_text = embedder.enrich_startup_text(
            name=s.get("name", ""),
            description=s.get("description", ""),
            category=s.get("category", ""),
            tags=s.get("tags", [])
        )
        ids.append(startup_id)
        texts.append(enriched_text)
        metadatas.append({
            "name": s.get("name", ""),
            "description": s.get("description", ""),
            "category": s.get("category", ""),
            "tags": ",".join(s.get("tags", [])),
            "founded_year": s.get("founded_year", 0),
            "funding_stage": s.get("funding_stage", ""),
            "status": s.get("status", ""),
            "url": s.get("url", "")
        })

    # Batch embed
    logger.info("Generating embeddings for all startups...")
    embeddings = embedder.embed_batch(texts)

    # Store in ChromaDB
    vector_store.add_startups(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
    logger.info(f"Seeding complete. {vector_store.get_count()} startups in vector store.")
