# 🚀 Multi-Strategy RAG Chatbot

A production-quality, fully responsive Retrieval-Augmented Generation (RAG) chatbot built with LangChain, Groq, ChromaDB, and Streamlit.

## ✨ Features

- **Multi-format Document Support**: Upload PDF, DOCX, TXT, CSV, PPTX, XLSX, MD, HTML, JSON, XML files
- **Three RAG Strategies**:
  - 🔵 **VectorRAG**: Pure semantic similarity search
  - 🟣 **HybridRAG**: Semantic + keyword (BM25) search
  - 🟠 **MultiRAG**: Multi-query retrieval with query expansion
- **Groq LLM Integration**: Free tier models including Llama 3, Mixtral, and Gemma
- **Beautiful Responsive UI**: Works on desktop, tablet, and mobile devices
- **Persistent Vector Store**: ChromaDB persists documents across sessions
- **Source Attribution**: See exactly which documents and pages informed each answer
- **Duplicate Detection**: Avoids re-indexing already processed files
- **Conversation Memory**: Maintains context for follow-up questions

## 📋 Prerequisites

- Python 3.10 or higher
- A free Groq API key (get one at [console.groq.com](https://console.groq.com))

## 🛠️ Installation

1. **Clone the repository** (or download the files):
   ```bash
   git clone <repository-url>
   cd rag-chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your Groq API key:
     ```env
     GROQ_API_KEY=your_groq_api_key_here
     EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
     CHROMA_PERSIST_DIR=./chroma_db
     COLLECTION_NAME=rag_documents
     ```

## 🚀 Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Using the chatbot**:
   - Enter your Groq API key in the sidebar (if not already in `.env`)
   - Select a Groq model from the dropdown
   - Choose a RAG strategy:
     - **VectorRAG**: Best for semantic understanding
     - **HybridRAG**: Best for keyword-specific queries
     - **MultiRAG**: Best for complex questions needing multiple perspectives
   - Upload your documents using the file uploader (multiple files supported)
   - Click "Process Documents" to index your files
   - Ask questions in the chat interface
   - View source documents by expanding the "📎 Sources" section under each answer

## 📁 Project Structure

```
rag-chatbot/
│
├── app.py                         # Main Streamlit app entry point
├── requirements.txt               # All dependencies
├── .env.example                   # Environment variable template
├── .gitignore
├── README.md
│
├── config/
│   └── settings.py                # All config: model names, chunk size, etc.
│
├── core/
│   ├── __init__.py
│   ├── document_loader.py         # Universal document loader (all file types)
│   ├── text_splitter.py           # Chunking strategies
│   ├── embeddings.py              # Embedding model setup
│   ├── vector_store.py            # ChromaDB setup and management
│   └── llm.py                     # Groq LLM setup via LangChain
│
├── rag/
│   ├── __init__.py
│   ├── vector_rag.py              # VectorRAG strategy
│   ├── hybrid_rag.py              # HybridRAG strategy (BM25 + vector)
│   ├── multi_rag.py               # MultiRAG strategy (multi-query)
│   └── rag_factory.py             # Factory to select RAG strategy
│
├── ui/
│   ├── __init__.py
│   ├── sidebar.py                 # Sidebar: upload, settings, strategy selector
│   ├── chat_interface.py          # Chat messages UI
│   └── styles.py                  # Custom CSS for responsive design
│
└── utils/
    ├── __init__.py
    ├── file_handler.py            # File saving, temp management
    └── helpers.py                 # Utility functions
```

## 🔧 Configuration

All configurable parameters are in `config/settings.py`:

- `GROQ_MODELS`: List of available Groq models
- `DEFAULT_MODEL`: Default model to use
- `CHUNK_SIZE`: Size of text chunks for processing (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `MAX_RETRIEVAL_DOCS`: Number of documents to retrieve (default: 5)
- `TEMPERATURE`: LLM temperature for creativity (default: 0.1)
- `EMBEDDING_MODEL`: HuggingFace embedding model (default: sentence-transformers/all-MiniLM-L6-v2)
- `CHROMA_PERSIST_DIR`: Directory for ChromaDB persistence (default: ./chroma_db)
- `COLLECTION_NAME`: Name of the ChromaDB collection (default: rag_documents)
- `SUPPORTED_EXTENSIONS`: List of supported file extensions

## 💡 How It Works

### Data Flow

1. **Document Processing**:
   - User uploads files via the sidebar
   - Files are saved temporarily and processed to avoid duplicates
   - `UniversalDocumentLoader` loads each file using the appropriate LangChain loader
   - `SmartTextSplitter` splits documents into chunks with overlap
   - `HuggingFaceEmbeddings` generates vector embeddings
   - `ChromaDB` stores the vectors with metadata
   - Original documents are stored in session state for BM25 (HybridRAG)

2. **Query Processing**:
   - User enters a question in the chat interface
   - Selected RAG strategy determines retrieval method:
     - **VectorRAG**: Uses ChromaDB semantic search only
     - **HybridRAG**: Combines BM25 keyword search with vector search (EnsembleRetriever)
     - **MultiRAG**: Uses MultiQueryRetriever to generate query variations
   - Retrieved context is passed to the Groq LLM with a system prompt
   - LLM generates an answer based solely on the provided context
   - Answer and source documents are displayed in the chat interface

### RAG Strategies Explained

- **VectorRAG**: Uses only semantic similarity search. Finds documents whose meaning is closest to the question, even if they don't share exact keywords.
- **HybridRAG**: Combines the precision of keyword matching (BM25) with the understanding of semantic search. Good for finding documents with specific terms while still capturing conceptual similarity.
- **MultiRAG**: Generates multiple variations of the user's question to capture different aspects of the query, then retrieves documents for each variation and combines results. Helps when the original question might not match document phrasing exactly.

## 🎨 UI/UX Features

- **Fully Responsive**: Works on mobile (375px), tablet (768px), and desktop (1440px+)
- **Chat Interface**: WhatsApp/ChatGPT style message bubbles with timestamps
- **Sidebar**: Collapsible on mobile, contains all controls and settings
- **Loading States**: Spinners and progress bars for user feedback
- **Toast Notifications**: Success/error messages for document processing
- **Source Attribution**: Expandable cards showing source files, page numbers, and relevant text excerpts
- **Strategy Badges**: Color-coded labels indicating which RAG strategy was used
- **Dark Mode Support**: Automatically adapts to Streamlit's theme
- **Custom Scrollbars**: Styled for better visual consistency

## 🔒 Security & Privacy

- All document processing happens locally on your machine
- No documents or API keys are sent to external servers (except to Groq for LLM inference)
- ChromaDB data is stored locally in the `./chroma_db` directory
- API keys are loaded from environment variables, never hardcoded

## 🐛 Troubleshooting

- **API Key Errors**: Make sure your Groq API key is correctly set in `.env` or entered in the sidebar
- **Document Processing Issues**: Check that your file format is supported and not corrupted
- **Slow Response Times**: The first question may be slower as the LLM loads; subsequent questions are faster
- **No Documents Found**: Ensure you've processed documents and that they contain readable text
- **ChromaDB Errors**: Try deleting the `./chroma_db` directory to reset the vector store

## 📚 Getting a Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to the API Keys section
4. Create a new API key
5. Copy the key and paste it into your `.env` file or the sidebar input

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for the RAG framework
- [Groq](https://groq.com/) for fast LLM inference
- [ChromaDB](https://www.trychroma.com/) for the vector database
- [Streamlit](https://streamlit.io/) for the web UI framework
- [Hugging Face](https://huggingface.co/) for the embedding models#   N e w _ C h a t _ B o t  
 