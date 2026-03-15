import logging
import os
import streamlit as st
from langchain_groq import ChatGroq
from config.settings import DEFAULT_MODEL, TEMPERATURE

logger = logging.getLogger(__name__)

@st.cache_resource
def get_llm(model_name: str = DEFAULT_MODEL, temperature: float = TEMPERATURE):
    """
    Get a Groq LLM instance, cached as a resource.

    Args:
        model_name: The name of the Groq model to use.
        temperature: The temperature for sampling.

    Returns:
        ChatGroq: The configured LLM instance.
    """
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        logger.error("GROQ_API_KEY not found in environment variables")
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    logger.info(f"Initializing Groq LLM with model: {model_name}, temperature: {temperature}")
    return ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model_name,
        temperature=temperature,
    )