# Centralized config — all tuneable parameters in one place
# Updated to use supported Groq models (llama-3.3-70b-versatile is recommended)
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]
DEFAULT_MODEL = "llama-3.3-70b-versatile"
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 300
MAX_RETRIEVAL_DOCS = 10
TEMPERATURE = 0.0
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "rag_documents"
SUPPORTED_EXTENSIONS = [
    ".pdf", ".docx", ".doc", ".txt", ".csv",
    ".pptx", ".ppt", ".xlsx", ".xls",
    ".md", ".html", ".htm", ".json", ".xml"
]