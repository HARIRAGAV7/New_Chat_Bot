import logging
import streamlit as st
from typing import Any

logger = logging.getLogger(__name__)

def initialize_session_state():
    """
    Initialize session state variables if they don't exist.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "documents_indexed" not in st.session_state:
        st.session_state.documents_indexed = False
    if "all_docs" not in st.session_state:
        st.session_state.all_docs = []
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "llm" not in st.session_state:
        st.session_state.llm = None
    if "selected_strategy" not in st.session_state:
        st.session_state.selected_strategy = "VectorRAG"
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()

def format_source_for_display(doc: Any) -> str:
    """
    Format a document source for display in the UI.

    Args:
        doc: A Document object.

    Returns:
        A formatted string with source and page information.
    """
    source = doc.metadata.get("source", "Unknown")
    # Extract just the filename from the path
    import os
    filename = os.path.basename(source)
    page = doc.metadata.get("page_number", "N/A")
    return f"{filename} (Page: {page})"

def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to a maximum length and add ellipsis if needed.

    Args:
        text: The text to truncate.
        max_length: The maximum length before truncation.

    Returns:
        The truncated text.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."