"""
chunker.py

Splits extracted document text into overlapping chunks
for Retrieval-Augmented Generation (RAG).

Dependencies:
    pip install langchain-text-splitters
"""

from __future__ import annotations

import uuid
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CHUNK_SIZE, CHUNK_OVERLAP


def create_chunks(
    document: dict[str, Any],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[dict[str, Any]]:
    """
    Split a document into overlapping chunks.

    Args:
        document:
            Dictionary returned by loader.py.

        chunk_size:
            Maximum number of characters in each chunk.

        chunk_overlap:
            Number of overlapping characters between chunks.

    Returns:
        A list of chunk dictionaries.
    """

    # ---------------------------------------------------------
    # Validate input
    # ---------------------------------------------------------

    if not isinstance(document, dict):
        raise TypeError("Document must be a dictionary.")

    required_keys = {"id", "filename", "text"}

    missing = required_keys - document.keys()
    if missing:
        raise ValueError(f"Missing required document keys: {', '.join(sorted(missing))}")

    text = document["text"]

    if not isinstance(text, str):
        raise TypeError("Document text must be a string.")

    if not text.strip():
        return []

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    # ---------------------------------------------------------
    # Initialize text splitter
    # ---------------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    split_texts = splitter.split_text(text)

    # ---------------------------------------------------------
    # Build chunk metadata
    # ---------------------------------------------------------

    chunks: list[dict[str, Any]] = []

    search_start = 0

    for index, chunk_text in enumerate(split_texts, start=1):

        start_index = text.find(chunk_text, search_start)

        if start_index == -1:
            start_index = search_start

        end_index = start_index + len(chunk_text)

        # Advance search position while accounting for overlap
        step = max(1, chunk_size - chunk_overlap)
        search_start = max(search_start, start_index + step)

        chunk = {
            "chunk_id": str(uuid.uuid4()),
            "document_id": document["id"],
            "filename": document["filename"],
            "chunk_number": index,
            "text": chunk_text,
            "word_count": len(chunk_text.split()),
            "character_count": len(chunk_text),
            "start_index": start_index,
            "end_index": end_index,
        }

        chunks.append(chunk)

    return chunks


# ---------------------------------------------------------
# Standalone Test
# ---------------------------------------------------------

if __name__ == "__main__":

    sample_document = {
        "id": str(uuid.uuid4()),
        "filename": "sample.pdf",
        "text": (
            "Artificial Intelligence is transforming industries. "
            "Machine learning enables computers to learn from data. "
            "Deep learning is a subset of machine learning. "
        )
        * 300,
    }

    chunks = create_chunks(sample_document)

    print("=" * 60)
    print("ContextHub Chunker Test")
    print("=" * 60)

    print(f"Total Chunks : {len(chunks)}")

    for chunk in chunks[:3]:
        print("-" * 60)
        print(f"Chunk Number : {chunk['chunk_number']}")
        print(f"Chunk ID     : {chunk['chunk_id']}")
        print(f"Words        : {chunk['word_count']}")
        print(f"Characters   : {chunk['character_count']}")
        print(f"Range        : [{chunk['start_index']} : {chunk['end_index']}]")
        print()
        print(chunk["text"][:200])
        print()