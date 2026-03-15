import logging
from typing import List, Dict, Any
from langchain_core.documents import Document
from .vector_rag import VectorRAGChain
from .hybrid_rag import HybridRAGChain
from .multi_rag import MultiRAGChain

logger = logging.getLogger(__name__)

class RAGFactory:
    """
    Factory class to create the appropriate RAG chain based on strategy.
    """

    @staticmethod
    def get_chain(strategy: str, retriever, llm, all_docs: List[Document] = None):
        """
        Get a RAG chain instance based on the strategy name.

        Args:
            strategy: The RAG strategy to use. Options: "VectorRAG", "HybridRAG", "MultiRAG".
            retriever: A LangChain retriever (e.g., from ChromaDB).
            llm: A LangChain LLM instance (e.g., ChatGroq).
            all_docs: List of all Document objects (required for HybridRAG).

        Returns:
            A RAG chain instance (VectorRAGChain, HybridRAGChain, or MultiRAGChain).

        Raises:
            ValueError: If an unsupported strategy is provided.
        """
        logger.info(f"Creating RAG chain for strategy: {strategy}")
        if strategy == "VectorRAG":
            return VectorRAGChain(retriever, llm)
        elif strategy == "HybridRAG":
            if all_docs is None:
                raise ValueError("all_docs is required for HybridRAG strategy")
            return HybridRAGChain(retriever, llm, all_docs)
        elif strategy == "MultiRAG":
            return MultiRAGChain(retriever, llm)
        else:
            raise ValueError(f"Unsupported RAG strategy: {strategy}. Choose from 'VectorRAG', 'HybridRAG', 'MultiRAG'.")