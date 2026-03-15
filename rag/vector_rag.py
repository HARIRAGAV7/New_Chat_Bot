import logging
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)

class VectorRAGChain:
    """
    VectorRAG chain that uses pure semantic search via ChromaDB retriever.
    """

    def __init__(self, retriever, llm):
        """
        Initialize the VectorRAG chain.

        Args:
            retriever: A LangChain retriever (e.g., from ChromaDB).
            llm: A LangChain LLM instance (e.g., ChatGroq).
        """
        self.retriever = retriever
        self.llm = llm
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
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
        logger.info("Initialized VectorRAGChain")

    def invoke(self, query: str) -> Dict[str, Any]:
        """
        Invoke the chain with a query.

        Args:
            query: The user's question.

        Returns:
            A dictionary with keys: 'answer', 'source_documents', 'strategy'.
        """
        logger.info(f"Invoking VectorRAGChain with query: {query}")
        result = self.qa_chain.invoke({"query": query})
        # The result from RetrievalQA is a dict with 'result' and 'source_documents'
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"],
            "strategy": "VectorRAG"
        }