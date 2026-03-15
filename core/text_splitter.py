import logging
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

logger = logging.getLogger(__name__)

class SmartTextSplitter:
    """
    Smart text splitter that uses RecursiveCharacterTextSplitter and adds chunk index metadata.
    """

    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks and add chunk index metadata.

        Args:
            documents: List of Document objects to split.

        Returns:
            List of chunked Document objects with metadata.
        """
        logger.info(f"Splitting {len(documents)} documents into chunks")
        chunks = self.text_splitter.split_documents(documents)
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i
        logger.info(f"Created {len(chunks)} chunks")
        return chunks