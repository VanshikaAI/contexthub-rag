"""
loader.py

Handles PDF loading and text extraction.

Dependencies:
    pip install pypdf
"""

from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Any, BinaryIO, Union

from pypdf import PdfReader
from pypdf.errors import PdfReadError

logger = logging.getLogger(__name__)

# Average adult reading speed (words per minute)
_WORDS_PER_MINUTE = 200


def load_pdf(pdf_file: Union[str, Path, BinaryIO]) -> dict[str, Any]:
    """
    Extract text and document statistics from a PDF.

    Args:
        pdf_file:
            A file path (str or Path) or a binary file-like object.

    Returns:
        Dictionary containing:
            id               - Unique document identifier (UUID4 string)
            filename         - Original file name
            text             - Extracted text
            pages            - Total page count
            words            - Word count
            characters       - Character count
            reading_time     - Estimated reading time (minutes)
            text_extracted   - True if any text was extracted

    Raises:
        FileNotFoundError:
            If the supplied file path does not exist.

        ValueError:
            If the file is not a valid, readable, or unencrypted PDF.
    """

    # Generate a unique document ID
    document_id = str(uuid.uuid4())

    # -------------------------------------------------------------
    # Validate input and determine filename
    # -------------------------------------------------------------

    if isinstance(pdf_file, (str, Path)):
        path = Path(pdf_file)

        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError(f"File does not have a .pdf extension: {path}")

        filename = path.name

    else:
        raw_name = getattr(pdf_file, "name", "") or ""
        filename = Path(raw_name).name if raw_name else "uploaded_document.pdf"

    # -------------------------------------------------------------
    # Read PDF
    # -------------------------------------------------------------

    try:
        reader = PdfReader(pdf_file)

    except PdfReadError as exc:
        raise ValueError(
            f"Malformed or unreadable PDF '{filename}': {exc}"
        ) from exc

    except Exception as exc:
        raise ValueError(
            f"Could not open PDF '{filename}': {exc}"
        ) from exc

    # -------------------------------------------------------------
    # Reject encrypted PDFs
    # -------------------------------------------------------------

    if reader.is_encrypted:
        raise ValueError(
            f"PDF '{filename}' is encrypted. Please decrypt it before uploading."
        )

    # -------------------------------------------------------------
    # Guard against empty PDFs
    # -------------------------------------------------------------

    if len(reader.pages) == 0:
        raise ValueError(f"PDF '{filename}' contains no pages.")

    # -------------------------------------------------------------
    # Extract text
    # -------------------------------------------------------------

    extracted_pages: list[str] = []

    for page_number, page in enumerate(reader.pages, start=1):

        try:
            page_text = page.extract_text() or ""

        except Exception as exc:
            logger.warning(
                "Failed to extract text from page %d of '%s': %s",
                page_number,
                filename,
                exc,
            )
            page_text = ""

        if page_text.strip():
            extracted_pages.append(page_text)

    extracted_text = "\n".join(extracted_pages)

    # -------------------------------------------------------------
    # Warn if no text could be extracted
    # -------------------------------------------------------------

    if not extracted_text.strip():
        logger.warning(
            "No text extracted from '%s'. "
            "The PDF may be scanned or image-only.",
            filename,
        )

    # -------------------------------------------------------------
    # Calculate document statistics
    # -------------------------------------------------------------

    total_pages = len(reader.pages)

    word_count = (
        len(extracted_text.split())
        if extracted_text.strip()
        else 0
    )

    character_count = len(extracted_text)

    reading_time = (
        round(word_count / _WORDS_PER_MINUTE)
        if word_count
        else 0
    )

    # -------------------------------------------------------------
    # Return document information
    # -------------------------------------------------------------

    return {
        "id": document_id,
        "filename": filename,
        "text": extracted_text,
        "pages": total_pages,
        "words": word_count,
        "characters": character_count,
        "reading_time": reading_time,
        "text_extracted": bool(extracted_text.strip()),
    }