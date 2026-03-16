import streamlit as st
from core.vector_store import VectorStoreManager

def render_sidebar():
    """
    Render the sidebar with all controls and information — professional edition.
    Returns a dictionary of the current settings and state.
    """
    with st.sidebar:
        # ── Brand header ──────────────────────────────────────────────
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-brand-icon">🧠</div>
                <div class="sidebar-brand-text">
                    <h2>RAG Chatbot</h2>
                    <span>Intelligent Document Assistant</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )



        # ── Knowledge base stats ──────────────────────────────────────
        st.markdown('<p class="sidebar-section-label">Knowledge Base</p>', unsafe_allow_html=True)
        vector_store = VectorStoreManager()
        if vector_store.collection_exists():
            stats = vector_store.get_collection_stats()
            count = stats.get('count', 0)
            st.markdown(
                f"""
                <div class="stat-card">
                    <span class="stat-icon">📚</span>
                    <span><span class="stat-value">{count}</span> chunks indexed</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="stat-card">
                    <span class="stat-icon">📭</span>
                    <span>No documents indexed yet</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button("🗑️ Clear Knowledge Base", use_container_width=True):
            if st.session_state.get('confirm_clear', False):
                vector_store.clear_collection()
                st.session_state['confirm_clear'] = False
                st.success("✅ Knowledge base cleared!")
                st.rerun()
            else:
                st.session_state['confirm_clear'] = True
                st.warning("⚠️ Click again to confirm deletion.")


        # ── Footer ────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="padding: 1.5rem 0 0.5rem 0; text-align: center;">
                <span style="font-size:0.65rem; color:#334155; letter-spacing:0.05em;">
                    Powered by LangChain · ChromaDB · Groq
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )