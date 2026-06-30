"""
config.py

Central configuration for ContextHub.
"""

from pathlib import Path

# ==========================================================
# Chunking Configuration
# ==========================================================

CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 200

# Guard: overlap must be less than chunk size
assert CHUNK_OVERLAP < CHUNK_SIZE, (
    f"CHUNK_OVERLAP ({CHUNK_OVERLAP}) must be less than CHUNK_SIZE ({CHUNK_SIZE})"
)

# ==========================================================
# Embedding Model
# ==========================================================

EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION: int = 384  # Matches all-MiniLM-L6-v2 output dim

# ==========================================================
# Vector Database
# ==========================================================

CHROMA_DB_PATH: Path = Path("data/chroma_db")
COLLECTION_NAME: str = "contexthub"

# ==========================================================
# Retrieval
# ==========================================================

TOP_K_RESULTS: int = 5
SIMILARITY_THRESHOLD: float = 0.25  # Minimum score to include a result (0.0–1.0)