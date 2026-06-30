# """
# app.py

# Main Streamlit application for ContextHub.
# """

# import sys
# from pathlib import Path

# # ==========================================================
# # Fix Python import path
# # ==========================================================

# PROJECT_ROOT = Path(__file__).resolve().parent.parent

# if str(PROJECT_ROOT) not in sys.path:
#     sys.path.insert(0, str(PROJECT_ROOT))

# import streamlit as st

# from src.loader import load_pdf
# from src.chunker import create_chunks
# from src.config import CHUNK_SIZE, CHUNK_OVERLAP

# # ==========================================================
# # Streamlit Page Configuration
# # ==========================================================

# st.set_page_config(
#     page_title="ContextHub",
#     page_icon="📚",
#     layout="wide",
# )

# st.title("📚 ContextHub")
# st.caption("AI-Powered Knowledge Workspace")

# st.write(
#     "Upload a PDF document and let ContextHub analyze it. "
#     "The application loads the document, extracts text, "
#     "and splits it into semantic chunks for Retrieval-Augmented Generation (RAG)."
# )

# # ==========================================================
# # File Upload
# # ==========================================================

# uploaded_file = st.file_uploader(
#     "Choose a PDF file",
#     type=["pdf"],
# )

# # ==========================================================
# # Process Uploaded File
# # ==========================================================

# if uploaded_file is not None:

#     try:

#         with st.spinner("Processing document..."):

#             # Load PDF
#             document = load_pdf(uploaded_file)

#             # Create chunks
#             chunks = create_chunks(document)

#         st.success("✅ Document processed successfully!")

#         st.divider()

#         # ==========================================================
#         # Document Information
#         # ==========================================================

#         st.subheader("📄 Document Information")

#         col1, col2, col3, col4 = st.columns(4)

#         col1.metric("Pages", document["pages"])
#         col2.metric("Words", f"{document['words']:,}")
#         col3.metric("Characters", f"{document['characters']:,}")
#         col4.metric("Reading Time", f"{document['reading_time']} min")

#         st.markdown(f"**Filename:** {document['filename']}")
#         st.markdown(f"**Document ID:** `{document['id']}`")

#         if document["text_extracted"]:
#             st.success("✅ Text extracted successfully.")
#         else:
#             st.warning(
#                 "No text could be extracted. "
#                 "The PDF may be scanned or image-only."
#             )

#         st.divider()

#         # ==========================================================
#         # Chunk Statistics
#         # ==========================================================

#         st.subheader("✂️ Chunk Statistics")

#         c1, c2, c3 = st.columns(3)

#         c1.metric("Total Chunks", len(chunks))
#         c2.metric("Chunk Size", CHUNK_SIZE)
#         c3.metric("Chunk Overlap", CHUNK_OVERLAP)

#         # ==========================================================
#         # Chunk Preview
#         # ==========================================================

#         if chunks:

#             st.subheader("📦 Chunk Preview")

#             preview_count = min(3, len(chunks))

#             for chunk in chunks[:preview_count]:

#                 with st.expander(
#                     f"Chunk {chunk['chunk_number']} "
#                     f"({chunk['word_count']} words)"
#                 ):

#                     st.write(
#                         f"**Characters:** {chunk['character_count']}"
#                     )

#                     st.write(
#                         f"**Range:** "
#                         f"{chunk['start_index']} → {chunk['end_index']}"
#                     )

#                     st.text(chunk["text"])

#         else:

#             st.warning("No chunks were created.")

#         st.divider()

#         # ==========================================================
#         # Full Extracted Text
#         # ==========================================================

#         st.subheader("📖 Extracted Text Preview")

#         st.text_area(
#             "Document Text",
#             document["text"],
#             height=400,
#         )

#     except Exception as e:

#         st.error(f"Failed to process document: {e}")

#         st.info(
#             "Please upload a valid, readable PDF document."
#         )

"""
app.py

Main Streamlit application for ContextHub.
"""

from pathlib import Path
import sys

# ==========================================================
# Fix Python Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==========================================================
# Imports
# ==========================================================

import streamlit as st

from src.loader import load_pdf
from src.chunker import create_chunks
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

# ==========================================================
# Streamlit Page Configuration
# ==========================================================

st.set_page_config(
    page_title="ContextHub",
    page_icon="📚",
    layout="wide",
)

st.title("📚 ContextHub")
st.caption("AI-Powered Knowledge Workspace")

st.write(
    "Upload a PDF document and let ContextHub analyze it. "
    "The application loads the document, extracts text, "
    "and splits it into semantic chunks for Retrieval-Augmented Generation (RAG)."
)

# ==========================================================
# File Upload
# ==========================================================

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
)

# ==========================================================
# Process Uploaded File
# ==========================================================

if uploaded_file is not None:

    try:

        with st.spinner("Processing document..."):

            # Load PDF
            document = load_pdf(uploaded_file)

            # Create chunks
            chunks = create_chunks(document)

        st.success("✅ Document processed successfully!")

        st.divider()

        # ==========================================================
        # Document Information
        # ==========================================================

        st.subheader("📄 Document Information")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Pages", document["pages"])
        col2.metric("Words", f"{document['words']:,}")
        col3.metric("Characters", f"{document['characters']:,}")
        col4.metric("Reading Time", f"{document['reading_time']} min")

        st.markdown(f"**Filename:** {document['filename']}")
        st.markdown(f"**Document ID:** `{document['id']}`")

        if document["text_extracted"]:
            st.success("✅ Text extracted successfully.")
        else:
            st.warning(
                "No text could be extracted. "
                "The PDF may be scanned or image-only."
            )

        st.divider()

        # ==========================================================
        # Chunk Statistics
        # ==========================================================

        st.subheader("✂️ Chunk Statistics")

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Chunks", len(chunks))
        c2.metric("Chunk Size", CHUNK_SIZE)
        c3.metric("Chunk Overlap", CHUNK_OVERLAP)

        # ==========================================================
        # Chunk Preview
        # ==========================================================

        if chunks:

            st.subheader("📦 Chunk Preview")

            preview_count = min(3, len(chunks))

            for chunk in chunks[:preview_count]:

                with st.expander(
                    f"Chunk {chunk['chunk_number']} "
                    f"({chunk['word_count']} words)"
                ):

                    st.write(f"**Characters:** {chunk['character_count']}")
                    st.write(
                        f"**Range:** {chunk['start_index']} → {chunk['end_index']}"
                    )
                    st.text(chunk["text"])

        else:

            st.warning("No chunks were created.")

        st.divider()

        # ==========================================================
        # Extracted Text Preview
        # ==========================================================

        st.subheader("📖 Extracted Text Preview")

        st.text_area(
            "Document Text",
            document["text"],
            height=400,
        )

    except Exception as e:

        st.error(f"Failed to process document: {e}")

        st.info(
            "Please upload a valid, readable PDF document."
        )