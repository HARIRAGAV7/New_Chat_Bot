import logging
from typing import List
from langchain_core.documents import Document
import chromadb
from langchain_chroma import Chroma
from config.settings import CHROMA_PERSIST_DIR, COLLECTION_NAME
from core.embeddings import get_embeddings

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """
    Manages the ChromaDB vector store for storing and retrieving document embeddings.
    """

    def __init__(self):
        """
        Initialize the ChromaDB client and vector store.
        """
        self.embeddings = get_embeddings()
        self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
        self.vector_store = Chroma(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
        )
        logger.info(f"Initialized ChromaDB with persist directory: {CHROMA_PERSIST_DIR}")

    def add_documents(self, docs: List[Document]) -> None:
        """
        Add documents to the vector store.

        Args:
            docs: List of Document objects to add.
        """
        if not docs:
            logger.warning("No documents to add")
            return
        logger.info(f"Adding {len(docs)} documents to vector store")
        self.vector_store.add_documents(docs)
        logger.info("Documents added successfully")

    def get_retriever(self, k: int = 5):
        """
        Get a retriever for the vector store.

        Args:
            k: Number of documents to retrieve.

        Returns:
            A LangChain retriever.
        """
        logger.info(f"Getting retriever with k={k}")
        return self.vector_store.as_retriever(search_kwargs={"k": k})

    def get_collection_stats(self) -> dict:
        """
        Get statistics about the collection.

        Returns:
            A dictionary with collection statistics.
        """
        collection = self.client.get_collection(name=COLLECTION_NAME)
        count = collection.count()
        logger.info(f"Collection '{COLLECTION_NAME}' has {count} documents")
        return {"count": count, "collection_name": COLLECTION_NAME}

    def clear_collection(self) -> None:
        """
        Clear all documents from the collection.
        """
        logger.info(f"Clearing collection: {COLLECTION_NAME}")
        self.client.delete_collection(name=COLLECTION_NAME)
        # Recreate the collection to avoid issues
        self.vector_store = Chroma(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
        )
        logger.info("Collection cleared and recreated")

    def collection_exists(self) -> bool:
        """
        Check if the collection exists and has any documents.

        Returns:
            True if the collection exists and has at least one document, False otherwise.
        """
        try:
            collection = self.client.get_collection(name=COLLECTION_NAME)
            return collection.count() > 0
        except Exception:
            return False