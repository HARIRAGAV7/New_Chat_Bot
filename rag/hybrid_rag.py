import logging
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

logger = logging.getLogger(__name__)

class HybridRAGChain:
    """
    HybridRAG chain that combines BM25 (keyword) and vector (semantic) search.
    """

    def __init__(self, vector_retriever, llm, all_docs: List[Document]):
        """
        Initialize the HybridRAG chain.

        Args:
            vector_retriever: A LangChain retriever for vector search (e.g., from ChromaDB).
            llm: A LangChain LLM instance (e.g., ChatGroq).
            all_docs: List of all Document objects (for BM25 retriever).
        """
        self.llm = llm
        # Create BM25 retriever from the all_docs
        self.bm25_retriever = BM25Retriever.from_documents(all_docs)
        self.bm25_retriever.k = 5  # default, can be adjusted
        # We'll set the vector retriever's k as well
        self.vector_retriever = vector_retriever
        if hasattr(self.vector_retriever, 'search_kwargs'):
            # If it's a Chroma retriever, we can set k via search_kwargs
            pass
        else:
            # Assume it's already configured
            pass

        # Create ensemble retriever with weights [0.4, 0.6] for BM25 and Vector respectively
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, self.vector_retriever],
            weights=[0.4, 0.6]
        )

        self.prompt = PromptTemplate(
            template="""You are a helpful assistant. Answer only based on the provided context. 
            If the answer is not in the context, say 'I don't have enough information in the uploaded documents to answer this.'.

            Context: {context}

            Question: {question}

            Answer:""",
            input_variables=["context", "question"]
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.ensemble_retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
        logger.info("Initialized HybridRAGChain")

    def invoke(self, query: str) -> Dict[str, Any]:
        """
        Invoke the chain with a query.

        Args:
            query: The user's question.

        Returns:
            A dictionary with keys: 'answer', 'source_documents', 'strategy'.
        """
        logger.info(f"Invoking HybridRAGChain with query: {query}")
        result = self.qa_chain.invoke({"query": query})
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"],
            "strategy": "HybridRAG"
        }