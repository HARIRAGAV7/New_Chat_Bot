import streamlit as st
import os
from dotenv import load_dotenv
from ui.styles import inject_custom_css
from ui.sidebar import render_sidebar
from ui.chat_interface import render_chat
from utils.helpers import initialize_session_state
from core.vector_store import VectorStoreManager
from core.llm import get_llm
from utils.file_handler import save_uploaded_files, load_and_split_files
from config.settings import (
    DEFAULT_MODEL, CHUNK_SIZE, CHUNK_OVERLAP,
    MAX_RETRIEVAL_DOCS, TEMPERATURE,
)

# Load environment variables
load_dotenv()

def main():
    """
    Main function to run the RAG chatbot application.
    """
    # ── Page config ───────────────────────────────────────────────────
    st.set_page_config(
        layout="wide",
        page_title="RAG Chatbot — Intelligent Document Assistant",
        page_icon="🧠",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": None,
            "Report a bug": None,
            "About": "**RAG Chatbot** — Powered by LangChain, ChromaDB & Groq.",
        },
    )

    # ── Inject custom CSS (dark professional theme) ───────────────────
    inject_custom_css()

    # ── Session state init ────────────────────────────────────────────
    initialize_session_state()

    # ── Sidebar ───────────────────────────────────────────────────────
    render_sidebar()

    # ── File processing ───────────────────────────────────────────────
    uploaded_files = st.session_state.get("uploaded_files_to_process")
    if uploaded_files:
        with st.spinner("⚙️ Processing documents…"):
            file_paths = save_uploaded_files(uploaded_files)

            if file_paths:
                all_docs, chunks = load_and_split_files(file_paths)

                if chunks:
                    vector_store = VectorStoreManager()
                    vector_store.add_documents(chunks)

                    st.session_state.vector_store       = vector_store
                    st.session_state.all_docs           = all_docs
                    st.session_state.documents_indexed  = True

                    st.success(
                        f"✅ Successfully processed **{len(uploaded_files)}** file(s) "
                        f"into **{len(chunks)}** chunks!"
                    )
                else:
                    st.error("❌ No content could be extracted from the uploaded files.")
            else:
                st.info("ℹ️ No new files to process — all files were already indexed.")

        if 'uploaded_files_to_process' in st.session_state:
            del st.session_state['uploaded_files_to_process']
        st.rerun()

    # ── LLM init ──────────────────────────────────────────────────────
    # Re-initialize LLM if config temperature differs from session to enforce accuracy
    if st.session_state.llm is None or st.session_state.get('temperature') != TEMPERATURE:
        try:
            st.session_state.llm = get_llm(
                model_name=DEFAULT_MODEL,
                temperature=TEMPERATURE,
            )
        except Exception as e:
            st.error(f"❌ Failed to initialize LLM: {str(e)}")

    # ── Apply config defaults into session state ───────────────────────
    st.session_state.selected_strategy = "MultiRAG"
    st.session_state.chunk_size        = CHUNK_SIZE
    st.session_state.chunk_overlap     = CHUNK_OVERLAP
    st.session_state.max_docs          = MAX_RETRIEVAL_DOCS
    st.session_state.temperature       = TEMPERATURE

    # ── Chat interface ─────────────────────────────────────────────────
    render_chat()


if __name__ == "__main__":
    main()