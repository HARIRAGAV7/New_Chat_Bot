import streamlit as st
from typing import List, Dict, Any
from langchain_core.documents import Document
import time
from config.settings import SUPPORTED_EXTENSIONS
from core.vector_store import VectorStoreManager

def render_chat():
    """
    Render the chat interface — professional dark edition.
    """
    # ── Initialize session state ──────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ── Page header ───────────────────────────────────────────────────
    st.markdown(
        """
        <div class="app-header">
            <h1>🧠 RAG Chatbot</h1>
            <p>Ask anything about your uploaded documents — powered by semantic retrieval & Groq LLM</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Document upload & Empty state ─────────────────────────────────
    vector_store = VectorStoreManager()
    has_docs = vector_store.collection_exists()

    if not has_docs:
        # Show large centered uploader when no docs exist
        st.markdown(
            """
            <div style="text-align: center; margin: 2rem 0 1rem 0;">
                <h3 style="margin-bottom: 0.5rem; color: #f8fafc;">📄 Upload Documents to Begin</h3>
                <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.5rem;">
                    Upload your files below to start chatting with your knowledge base.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            uploaded_files = st.file_uploader(
                "Drag & drop or click to upload",
                type=[ext.lstrip('.') for ext in SUPPORTED_EXTENSIONS],
                accept_multiple_files=True,
                help=f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}",
                label_visibility="collapsed",
                key="main_uploader_empty"
            )
            if uploaded_files:
                st.caption(f"📂 {len(uploaded_files)} file(s) selected")
                if st.button("🚀 Process Documents", type="primary", use_container_width=True):
                    st.session_state['uploaded_files_to_process'] = uploaded_files
                    st.rerun()
        st.divider()
    else:
        # Show mini uploader above chat if docs already exist
        with st.expander("📄 Upload More Documents"):
            uploaded_files = st.file_uploader(
                "Drag & drop or click to upload",
                type=[ext.lstrip('.') for ext in SUPPORTED_EXTENSIONS],
                accept_multiple_files=True,
                help=f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}",
                label_visibility="collapsed",
                key="main_uploader_more"
            )
            if uploaded_files:
                st.caption(f"📂 {len(uploaded_files)} file(s) selected")
                if st.button("🚀 Process Documents", type="primary", use_container_width=True):
                    st.session_state['uploaded_files_to_process'] = uploaded_files
                    st.rerun()

    # ── Display chat messages ─────────────────────────────────────────
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

            # Source documents expander
            if message["role"] == "assistant" and "sources" in message and message["sources"]:
                with st.expander(f"📎 {len(message['sources'])} source(s) used"):
                    for i, doc in enumerate(message["sources"]):
                        source  = doc.metadata.get("source", "Unknown")
                        page    = doc.metadata.get("page_number", "N/A")
                        content = doc.page_content[:200] + "…" if len(doc.page_content) > 200 else doc.page_content
                        st.markdown(
                            f"""
                            <div style="
                                background:rgba(15,23,42,0.6);
                                border:1px solid rgba(99,102,241,0.15);
                                border-radius:8px;
                                padding:0.65rem 0.85rem;
                                margin-bottom:0.5rem;
                            ">
                                <div style="font-weight:600; color:#818cf8; font-size:0.78rem; margin-bottom:0.3rem;">
                                    📄 Source {i+1}: {source}
                                    <span style="color:#475569; font-weight:400;"> — Page {page}</span>
                                </div>
                                <div style="color:#94a3b8; font-size:0.8rem; line-height:1.55; font-style:italic;">
                                    {content}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            # Strategy badge
            if message["role"] == "assistant":
                strategy = message.get("strategy", "")
                if strategy and strategy not in ("None", "Error", ""):
                    st.markdown(
                        f'<span class="strategy-badge {strategy}">⚡ {strategy}</span>',
                        unsafe_allow_html=True,
                    )

    # ── Chat input ────────────────────────────────────────────────────
    if prompt := st.chat_input("Ask anything about your documents…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # No documents indexed fallback
        vector_store = st.session_state.get('vector_store')
        if not vector_store or not vector_store.collection_exists():
            with st.chat_message("assistant"):
                st.warning("📂 Please upload and process documents first to start asking questions.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Please upload and process documents first to ask questions.",
                "sources": [],
                "strategy": "None",
            })
            return

        strategy = st.session_state.get('selected_strategy', 'VectorRAG')
        llm      = st.session_state.get('llm')
        all_docs = st.session_state.get('all_docs', [])

        # LLM not ready fallback
        if not llm:
            with st.chat_message("assistant"):
                st.error("❌ LLM not initialized. Please ensure `GROQ_API_KEY` is set in the `.env` file.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "LLM not initialized. Please ensure GROQ_API_KEY is set in the .env file.",
                "sources": [],
                "strategy": "Error",
            })
            return

        # Generate answer
        with st.chat_message("assistant"):
            with st.spinner(f"Thinking with {strategy}…"):
                try:
                    retriever = vector_store.get_retriever(k=st.session_state.get('max_docs', 5))

                    from rag.rag_factory import RAGFactory
                    rag_chain = RAGFactory.get_chain(
                        strategy=strategy,
                        retriever=retriever,
                        llm=llm,
                        all_docs=all_docs,
                    )

                    result = rag_chain.invoke(prompt)
                    st.write(result["answer"])

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["source_documents"],
                        "strategy": result["strategy"],
                    })

                except Exception as e:
                    error_msg = str(e)
                    if "model_decommissioned" in error_msg:
                        error_msg = "The selected model has been decommissioned. Please contact support."
                    elif "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                        error_msg = "Authentication failed. Please check your Groq API key in the .env file."
                    elif "rate limit" in error_msg.lower():
                        error_msg = "Rate limit exceeded. Please try again in a moment."

                    st.error(f"❌ {error_msg}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"An error occurred: {error_msg}",
                        "sources": [],
                        "strategy": "Error",
                    })

    # ── Clear chat ────────────────────────────────────────────────────
    if st.session_state.messages:
        col1, col2, col3 = st.columns([3, 1, 3])
        with col2:
            if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()