import logging
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL

logger = logging.getLogger(__name__)

@st.cache_resource
def get_embeddings():
    """
    Get the HuggingFace embedding model, cached as a resource.
    Returns:
        HuggingFaceEmbeddings: The embedding model instance.
    """
    logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)