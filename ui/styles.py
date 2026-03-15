import streamlit as st

def inject_custom_css():
    """
    Inject custom CSS for the RAG chatbot UI.
    This function should be called at the beginning of the app to apply styles.
    """
    st.markdown(
        """
        <style>
        /* Responsive layout that works on all screen sizes */
        .main .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 2rem;
            margin: 0 auto;
        }
        /* Mobile breakpoint: stack sidebar below main on <768px */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
            /* Make the sidebar take full width on mobile */
            [data-testid="stSidebar"] {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
        /* Chat bubbles: user = right-aligned blue, assistant = left-aligned gray */
        .stChatMessage {
            padding: 0.5rem 1rem;
            border-radius: 1rem;
            margin-bottom: 0.5rem;
            max-width: 80%;
            word-wrap: break-word;
        }
        .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
            /* User messages (assuming odd indices are user, even are assistant) */
            background-color: #e3f2fd;
            margin-left: auto;
            margin-right: 0;
            border-bottom-right-radius: 0.25rem;
        }
        .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
            /* Assistant messages */
            background-color: #f5f5f5;
            margin-right: auto;
            margin-left: 0;
            border-bottom-left-radius: 0.25rem;
        }
        /* File uploader: dashed border, drag-drop zone styling */
        .stFileUploader > div {
            border: 2px dashed #6366f1;
            border-radius: 0.5rem;
            padding: 2rem;
            text-align: center;
            background-color: #f8fafc;
        }
        .stFileUploader > div:hover {
            border-color: #4f46e5;
            background-color: #f1f5f9;
        }
        /* Sidebar: clean white card with shadow */
        [data-testid="stSidebar"] {
            background-color: white;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            padding: 1rem;
        }
        /* Smooth scroll for chat history */
        .stChatFloatingInputContainer {
            bottom: 2rem;
        }
        /* Custom scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        /* Loading spinner animation */
        .stSpinner > div {
            border-color: #6366f1 transparent #6366f1 transparent;
        }
        /* Source document expandable cards */
        .streamlit-expanderHeader {
            font-size: 0.9rem;
            font-weight: 600;
            color: #334155;
        }
        /* Strategy badge chips (colored labels per RAG type) */
        .strategy-badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .strategy-badge.VectorRAG {
            background-color: #dbeafe;
            color: #1e40af;
        }
        .strategy-badge.HybridRAG {
            background-color: #ede9fe;
            color: #5b21b6;
        }
        .strategy-badge.MultiRAG {
            background-color: #fed7aa;
            color: #9a3412;
        }
        /* Responsive font sizes using clamp() */
        h1, h2, h3, h4, h5, h6 {
            line-height: 1.2;
        }
        h1 {
            font-size: clamp(1.5rem, 4vw, 2.5rem);
        }
        h2 {
            font-size: clamp(1.25rem, 4vw, 2rem);
        }
        h3 {
            font-size: clamp(1.125rem, 4vw, 1.75rem);
        }
        /* Dark mode support using Streamlit's theme variables */
        /* Streamlit automatically adjusts colors in dark mode, but we can override if needed */
        @media (prefers-color-scheme: dark) {
            .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
                background-color: #1e293b;
                color: #f8fafc;
            }
            .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
                background-color: #334155;
                color: #f8fafc;
            }
            [data-testid="stSidebar"] {
                background-color: #0f172a;
                color: #f8fafc;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )