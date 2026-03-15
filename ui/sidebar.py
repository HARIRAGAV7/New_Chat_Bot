import streamlit as st
import os
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP, MAX_RETRIEVAL_DOCS, TEMPERATURE, SUPPORTED_EXTENSIONS, DEFAULT_MODEL
from core.vector_store import VectorStoreManager

def render_sidebar():
    """
    Render the sidebar with all the controls and information.
    Returns a dictionary of the current settings and state.
    """
    with st.sidebar:
        st.title("🧠 RAG Chatbot")
        st.caption("Your intelligent document assistant")

        # RAG Strategy selector
        st.subheader("🤖 Retrieval Strategy")
        strategy = st.radio(
            "Select RAG strategy",
            options=["VectorRAG", "HybridRAG", "MultiRAG"],
            format_func=lambda x: {
                "VectorRAG": "🔵 VectorRAG — Pure semantic search",
                "HybridRAG": "🟣 HybridRAG — Semantic + keyword search",
                "MultiRAG": "🟠 MultiRAG — Multi-query expansion"
            }[x],
            help="Choose the retrieval-augmented generation strategy"
        )

        # Strategy info tooltip (using an expander)
        with st.expander("ℹ️ About the Strategies"):
            st.write("""
            - **VectorRAG**: Uses only semantic similarity search (vector embeddings) to find relevant documents.
            - **HybridRAG**: Combines keyword-based (BM25) and semantic search for better recall.
            - **MultiRAG**: Generates multiple query variations to capture different aspects of the question.
            """)

        # Document Upload
        st.subheader("📄 Document Upload")
        uploaded_files = st.file_uploader(
            "Upload your documents",
            type=[ext.lstrip('.') for ext in SUPPORTED_EXTENSIONS],  # Remove the dot for st.file_uploader
            accept_multiple_files=True,
            help=f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

        # Process Documents button
        if st.button("🚀 Process Documents", type="primary"):
            if not uploaded_files:
                st.warning("Please upload at least one document.")
            else:
                # We'll return the uploaded files to be processed in the main app
                st.session_state['uploaded_files_to_process'] = uploaded_files
                st.rerun()  # Rerun to trigger processing in the main app

        # Collection stats
        st.subheader("📊 Knowledge Base")
        vector_store = VectorStoreManager()
        if vector_store.collection_exists():
            stats = vector_store.get_collection_stats()
            st.info(f"📚 {stats['count']} documents indexed")
        else:
            st.info("📚 No documents indexed yet")

        # Clear Knowledge Base button
        if st.button("🗑️ Clear Knowledge Base", type="secondary"):
            if st.session_state.get('confirm_clear', False):
                vector_store.clear_collection()
                st.session_state['confirm_clear'] = False
                st.success("Knowledge base cleared!")
                st.rerun()
            else:
                st.session_state['confirm_clear'] = True
                st.warning("Click again to confirm deletion of all indexed documents.")

        # Settings expander
        with st.expander("⚙️ Advanced Settings"):
            chunk_size = st.slider(
                "Chunk size",
                min_value=200,
                max_value=2000,
                value=CHUNK_SIZE,
                step=100,
                help="Size of text chunks for processing"
            )
            chunk_overlap = st.slider(
                "Chunk overlap",
                min_value=0,
                max_value=500,
                value=CHUNK_OVERLAP,
                step=50,
                help="Overlap between consecutive chunks"
            )
            max_docs = st.slider(
                "Max retrieval documents",
                min_value=1,
                max_value=10,
                value=MAX_RETRIEVAL_DOCS,
                help="Maximum number of documents to retrieve for context"
            )
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=TEMPERATURE,
                step=0.1,
                help="Creativity of the LLM (0.0 = deterministic, 1.0 = creative)"
            )

            # Store these in session state to be used by the main app
            st.session_state['chunk_size'] = chunk_size
            st.session_state['chunk_overlap'] = chunk_overlap
            st.session_state['max_docs'] = max_docs
            st.session_state['temperature'] = temperature

    # Return the current settings as a dictionary
    return {
        "strategy": strategy,
        "uploaded_files": st.session_state.get('uploaded_files_to_process', None),
        "chunk_size": st.session_state.get('chunk_size', CHUNK_SIZE),
        "chunk_overlap": st.session_state.get('chunk_overlap', CHUNK_OVERLAP),
        "max_docs": st.session_state.get('max_docs', MAX_RETRIEVAL_DOCS),
        "temperature": st.session_state.get('temperature', TEMPERATURE),
    }