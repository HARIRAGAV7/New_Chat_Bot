import streamlit as st

def inject_custom_css():
    """
    Inject custom CSS for the RAG chatbot UI — professional dark theme.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ─── Global Reset ───────────────────────────────────────────── */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* ─── App Background ─────────────────────────────────────────── */
        .stApp {
            background: linear-gradient(135deg, #0d0f1a 0%, #111827 60%, #0d1117 100%);
            min-height: 100vh;
        }

        /* ─── Main Container ─────────────────────────────────────────── */
        .main .block-container {
            max-width: 1000px;
            padding: 1.5rem 2rem 6rem 2rem;
            margin: 0 auto;
        }

        /* ─── Page Header (injected via st.markdown) ─────────────────── */
        .app-header {
            text-align: center;
            padding: 2.5rem 1rem 1.5rem 1rem;
            margin-bottom: 1rem;
        }
        .app-header h1 {
            font-size: clamp(1.8rem, 4vw, 2.6rem);
            font-weight: 700;
            background: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.02em;
            margin: 0;
            line-height: 1.2;
        }
        .app-header p {
            color: #64748b;
            font-size: 0.95rem;
            margin-top: 0.5rem;
            font-weight: 400;
        }

        /* ─── Sidebar ────────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f1629 0%, #111827 100%) !important;
            border-right: 1px solid rgba(99, 102, 241, 0.15) !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding: 1.5rem 1rem;
        }
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {
            color: #cbd5e1 !important;
        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #f1f5f9 !important;
        }

        /* Sidebar logo area */
        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.5rem 0 1.5rem 0;
            border-bottom: 1px solid rgba(99, 102, 241, 0.2);
            margin-bottom: 1.25rem;
        }
        .sidebar-brand-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #6366f1, #a78bfa);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            box-shadow: 0 0 16px rgba(99,102,241,0.35);
        }
        .sidebar-brand-text h2 {
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            margin: 0 !important;
            background: linear-gradient(135deg, #818cf8, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .sidebar-brand-text span {
            font-size: 0.7rem !important;
            color: #475569 !important;
            font-weight: 400 !important;
        }

        /* Sidebar section labels */
        .sidebar-section-label {
            font-size: 0.65rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.1em !important;
            text-transform: uppercase !important;
            color: #475569 !important;
            margin: 1.25rem 0 0.5rem 0 !important;
        }

        /* ─── Strategy Radio Buttons ─────────────────────────────────── */
        [data-testid="stRadio"] > div {
            gap: 0.35rem;
        }
        [data-testid="stRadio"] label {
            background: rgba(30, 41, 59, 0.6) !important;
            border: 1px solid rgba(99, 102, 241, 0.15) !important;
            border-radius: 10px !important;
            padding: 0.55rem 0.75rem !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            font-size: 0.84rem !important;
        }
        [data-testid="stRadio"] label:hover {
            border-color: rgba(99, 102, 241, 0.5) !important;
            background: rgba(99, 102, 241, 0.08) !important;
        }

        /* ─── Buttons ────────────────────────────────────────────────── */
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            transition: all 0.2s ease !important;
            letter-spacing: 0.01em !important;
        }
        /* Primary button */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            border: none !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35) !important;
        }
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
        }
        /* Secondary / default button */
        .stButton > button:not([kind="primary"]) {
            background: rgba(30, 41, 59, 0.6) !important;
            border: 1px solid rgba(99, 102, 241, 0.25) !important;
            color: #94a3b8 !important;
        }
        .stButton > button:not([kind="primary"]):hover {
            border-color: rgba(239, 68, 68, 0.5) !important;
            color: #f87171 !important;
            background: rgba(239, 68, 68, 0.08) !important;
        }

        /* ─── Chat Input ─────────────────────────────────────────────── */
        .stChatInputContainer, [data-testid="stChatInput"] {
            background: #1e293b !important;
            border: 1px solid rgba(99, 102, 241, 0.25) !important;
            border-radius: 14px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
        }
        .stChatInputContainer:focus-within {
            border-color: rgba(99, 102, 241, 0.6) !important;
            box-shadow: 0 4px 20px rgba(99,102,241,0.15) !important;
        }
        [data-testid="stChatInput"] textarea {
            background: transparent !important;
            color: #f1f5f9 !important;
            font-family: 'Inter', sans-serif !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: #475569 !important;
        }

        /* ─── Chat Messages ─────────────────────────────────────────── */
        [data-testid="stChatMessage"] {
            background: rgba(15, 23, 42, 0.7) !important;
            border: 1px solid rgba(99, 102, 241, 0.1) !important;
            border-radius: 16px !important;
            padding: 1rem 1.25rem !important;
            margin-bottom: 0.75rem !important;
            backdrop-filter: blur(8px);
            transition: border-color 0.2s;
        }
        [data-testid="stChatMessage"]:hover {
            border-color: rgba(99, 102, 241, 0.25) !important;
        }
        /* User messages — subtle indigo tint */
        [data-testid="stChatMessage"][data-testid*="user"] {
            background: rgba(99, 102, 241, 0.08) !important;
            border-color: rgba(99, 102, 241, 0.2) !important;
        }

        /* ─── Chat Avatar ────────────────────────────────────────────── */
        [data-testid="stChatMessageAvatarUser"],
        [data-testid="stChatMessageAvatarAssistant"] {
            border-radius: 50% !important;
        }

        /* ─── Chat text ─────────────────────────────────────────────── */
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li {
            color: #cbd5e1 !important;
            font-size: 0.92rem !important;
            line-height: 1.65 !important;
        }
        [data-testid="stChatMessage"] code {
            background: rgba(99, 102, 241, 0.12) !important;
            color: #a78bfa !important;
            border-radius: 5px !important;
            padding: 0.1em 0.4em !important;
            font-size: 0.85em !important;
        }

        /* ─── Expander (Sources) ─────────────────────────────────────── */
        .streamlit-expanderHeader {
            background: rgba(30, 41, 59, 0.5) !important;
            border: 1px solid rgba(99, 102, 241, 0.15) !important;
            border-radius: 10px !important;
            color: #94a3b8 !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            transition: all 0.2s !important;
        }
        .streamlit-expanderHeader:hover {
            border-color: rgba(99, 102, 241, 0.4) !important;
            color: #818cf8 !important;
        }
        .streamlit-expanderContent {
            background: rgba(15, 23, 42, 0.5) !important;
            border: 1px solid rgba(99, 102, 241, 0.1) !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
        }

        /* ─── File Uploader ──────────────────────────────────────────── */
        [data-testid="stFileUploader"] {
            border-radius: 12px !important;
        }
        [data-testid="stFileUploader"] > div {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 2px dashed rgba(99, 102, 241, 0.35) !important;
            border-radius: 12px !important;
            transition: all 0.2s !important;
        }
        [data-testid="stFileUploader"] > div:hover {
            border-color: rgba(99, 102, 241, 0.7) !important;
            background: rgba(99, 102, 241, 0.05) !important;
        }

        /* ─── Sliders ────────────────────────────────────────────────── */
        [data-testid="stSlider"] [role="slider"] {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            box-shadow: 0 0 8px rgba(99,102,241,0.5) !important;
        }
        [data-testid="stSlider"] [data-testid="stSliderTrack"] {
            background: rgba(99,102,241,0.25) !important;
        }

        /* ─── Info / Success / Warning / Error boxes ─────────────────── */
        [data-testid="stAlert"] {
            border-radius: 10px !important;
            border-left: 3px solid !important;
            background: rgba(15,23,42,0.7) !important;
            font-size: 0.85rem !important;
        }

        /* ─── Strategy Badges ────────────────────────────────────────── */
        .strategy-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            margin-top: 0.5rem;
        }
        .strategy-badge.VectorRAG {
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }
        .strategy-badge.HybridRAG {
            background: rgba(167, 139, 250, 0.15);
            color: #a78bfa;
            border: 1px solid rgba(167, 139, 250, 0.3);
        }
        .strategy-badge.MultiRAG {
            background: rgba(251, 146, 60, 0.15);
            color: #fb923c;
            border: 1px solid rgba(251, 146, 60, 0.3);
        }
        .strategy-badge.Error {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        /* ─── Stat Card (Knowledge Base) ─────────────────────────────── */
        .stat-card {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 0.85rem 1rem;
            margin: 0.25rem 0;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 0.82rem;
            color: #94a3b8;
        }
        .stat-card .stat-icon {
            font-size: 1rem;
        }
        .stat-card .stat-value {
            font-weight: 700;
            color: #818cf8;
        }

        /* ─── Divider ────────────────────────────────────────────────── */
        hr {
            border-color: rgba(99, 102, 241, 0.15) !important;
            margin: 0.75rem 0 !important;
        }

        /* ─── Scrollbar ──────────────────────────────────────────────── */
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb {
            background: rgba(99, 102, 241, 0.3);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(99, 102, 241, 0.55);
        }

        /* ─── Spinner ────────────────────────────────────────────────── */
        [data-testid="stSpinner"] > div {
            border-top-color: #6366f1 !important;
        }

        /* ─── Mobile ─────────────────────────────────────────────────── */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem 0.75rem 5rem 0.75rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )