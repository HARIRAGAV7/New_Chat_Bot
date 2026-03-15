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
from config.settings import DEFAULT_MODEL

# Load environment variables
load_dotenv()

def main():
    """
    Main function to run the RAG chatbot application.
    """
    # Set page config
    st.set_page_config(
        layout="wide",
        page_title="RAG Chatbot",
        page_icon="🧠",
        initial_sidebar_state="expanded"
    )
    
    # Inject custom CSS
    inject_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar and get settings
    sidebar_settings = render_sidebar()
    
    # Handle file upload and processing
    uploaded_files = sidebar_settings.get("uploaded_files")
    if uploaded_files:
        with st.spinner("Processing documents..."):
            # Save uploaded files
            file_paths = save_uploaded_files(uploaded_files)
            
            if file_paths:
                # Load and split files
                all_docs, chunks = load_and_split_files(file_paths)
                
                if chunks:
                    # Initialize vector store and add documents
                    vector_store = VectorStoreManager()
                    vector_store.add_documents(chunks)
                    
                    # Update session state
                    st.session_state.vector_store = vector_store
                    st.session_state.all_docs = all_docs
                    st.session_state.documents_indexed = True
                    
                    # Show success message
                    st.success(f"Successfully processed {len(uploaded_files)} file(s) into {len(chunks)} chunks!")
                else:
                    st.error("No content could be extracted from the uploaded files.")
            else:
                st.info("No new files to process (all files were duplicates).")
        
        # Clear the uploaded files from session state to avoid reprocessing on rerun
        if 'uploaded_files_to_process' in st.session_state:
            del st.session_state['uploaded_files_to_process']
        st.rerun()
    
    # Initialize LLM if not already done - uses DEFAULT_MODEL from config/settings.py
    if st.session_state.llm is None:
        try:
            # API key is read from environment variable by get_llm()
            st.session_state.llm = get_llm(
                model_name=DEFAULT_MODEL,
                temperature=sidebar_settings.get('temperature', 0.1)
            )
        except Exception as e:
            st.error(f"Failed to initialize LLM: {str(e)}")
    
    # Update selected strategy in session state
    st.session_state.selected_strategy = sidebar_settings["strategy"]
    
    # Update other settings from sidebar
    st.session_state.chunk_size = sidebar_settings["chunk_size"]
    st.session_state.chunk_overlap = sidebar_settings["chunk_overlap"]
    st.session_state.max_docs = sidebar_settings["max_docs"]
    st.session_state.temperature = sidebar_settings["temperature"]
    
    # Render chat interface
    render_chat()

if __name__ == "__main__":
    main()