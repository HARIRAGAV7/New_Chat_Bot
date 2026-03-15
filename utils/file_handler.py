import logging
import os
import hashlib
import streamlit as st
from typing import List, Tuple
from core.document_loader import UniversalDocumentLoader
from core.text_splitter import SmartTextSplitter
from config.settings import SUPPORTED_EXTENSIONS

logger = logging.getLogger(__name__)

def save_uploaded_files(uploaded_files) -> List[str]:
    """
    Save uploaded files to a temporary directory and return the list of file paths.
    Also, avoid re-processing already processed files by checking a hash.

    Args:
        uploaded_files: List of uploaded files from st.file_uploader.

    Returns:
        List of file paths that were saved and are new (not previously processed).
    """
    # Create a temporary directory if it doesn't exist
    temp_dir = "./temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)

    saved_file_paths = []
    for uploaded_file in uploaded_files:
        # Generate a hash of the file content to detect duplicates
        file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()
        # Check if we have already processed this file (by hash) in this session
        if 'processed_files' not in st.session_state:
            st.session_state.processed_files = set()
        if file_hash in st.session_state.processed_files:
            logger.info(f"File {uploaded_file.name} already processed. Skipping.")
            continue

        # Save the file
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        saved_file_paths.append(file_path)
        # Mark as processed (by hash) so we don't process again in this session
        st.session_state.processed_files.add(file_hash)
        logger.info(f"Saved uploaded file: {file_path}")

    return saved_file_paths

def load_and_split_files(file_paths: List[str]) -> Tuple[List, List]:
    """
    Load and split the given files.

    Args:
        file_paths: List of file paths to load and split.

    Returns:
        A tuple (all_docs, chunks) where:
          all_docs: List of Document objects (before splitting) - used for BM25 in HybridRAG.
          chunks: List of Document objects (after splitting) - used for vector store.
    """
    if not file_paths:
        return [], []

    loader = UniversalDocumentLoader()
    splitter = SmartTextSplitter()

    all_docs = []
    chunks = []

    for file_path in file_paths:
        try:
            logger.info(f"Loading and splitting {file_path}")
            docs = loader.load(file_path)
            if not docs:
                logger.warning(f"No documents loaded from {file_path}")
                continue
            all_docs.extend(docs)
            file_chunks = splitter.split_documents(docs)
            chunks.extend(file_chunks)
            logger.info(f"Loaded {len(docs)} documents and split into {len(file_chunks)} chunks from {file_path}")
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            continue

    return all_docs, chunks