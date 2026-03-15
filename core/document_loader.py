import logging
from typing import List
from langchain_core.documents import Document

# Import all necessary loaders
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    UnstructuredHTMLLoader,
    UnstructuredFileLoader,
    JSONLoader,
)

# JSONLoader is actually in langchain_community.document_loaders, not a separate submodule
# But keeping the import explicit for clarity

logger = logging.getLogger(__name__)

class UniversalDocumentLoader:
    """
    Universal document loader that handles multiple file types.
    Uses appropriate LangChain loader based on file extension.
    """

    def __init__(self):
        # Mapping of file extensions to loader classes and their init args
        self.loaders = {
            '.pdf': (PyPDFLoader, {}),
            '.docx': (Docx2txtLoader, {}),
            '.doc': (Docx2txtLoader, {}),  # Assuming .doc can be handled by Docx2txtLoader
            '.txt': (TextLoader, {}),
            '.md': (TextLoader, {}),
            '.csv': (CSVLoader, {}),
            '.pptx': (UnstructuredPowerPointLoader, {}),
            '.ppt': (UnstructuredPowerPointLoader, {}),
            '.xlsx': (UnstructuredExcelLoader, {}),
            '.xls': (UnstructuredExcelLoader, {}),
            '.html': (UnstructuredHTMLLoader, {}),
            '.htm': (UnstructuredHTMLLoader, {}),
            '.json': (JSONLoader, {}),
            '.xml': (UnstructuredFileLoader, {}),
        }

    def load(self, file_path: str) -> List[Document]:
        """
        Load a document from the given file path.

        Args:
            file_path: Path to the file to load.

        Returns:
            List of Document objects.
        """
        import os
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext not in self.loaders:
            logger.warning(f"No specific loader for extension {ext}, falling back to UnstructuredFileLoader")
            loader_class, loader_args = UnstructuredFileLoader, {}
        else:
            loader_class, loader_args = self.loaders[ext]

        try:
            logger.info(f"Loading {file_path} with {loader_class.__name__}")
            loader = loader_class(file_path, **loader_args)
            documents = loader.load()

            # Add metadata: source, file_type, and page_number (if available)
            for i, doc in enumerate(documents):
                doc.metadata.update({
                    "source": file_path,
                    "file_type": ext[1:],  # remove the dot
                    "page_number": i + 1  # simple page number, adjust if loader provides it
                })
            return documents
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return []