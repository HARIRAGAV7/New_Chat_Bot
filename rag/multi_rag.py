import logging
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers import MultiQueryRetriever

logger = logging.getLogger(__name__)

class MultiRAGChain:
    """
    MultiRAG chain that uses MultiQueryRetriever for query expansion.
    """

    def __init__(self, vector_retriever, llm):
        """
        Initialize the MultiRAG chain.

        Args:
            vector_retriever: A LangChain retriever for vector search (e.g., from ChromaDB).
            llm: A LangChain LLM instance (e.g., ChatGroq) used to generate multiple queries.
        """
        self.llm = llm
        # Create a MultiQueryRetriever that uses the vector_retriever and the llm to generate multiple queries
        self.multiquery_retriever = MultiQueryRetriever.from_llm(
            retriever=vector_retriever,
            llm=llm
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
            retriever=self.multiquery_retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
        logger.info("Initialized MultiRAGChain")

    def invoke(self, query: str) -> Dict[str, Any]:
        """
        Invoke the chain with a query.

        Args:
            query: The user's question.

        Returns:
            A dictionary with keys: 'answer', 'source_documents', 'strategy'.
        """
        logger.info(f"Invoking MultiRAGChain with query: {query}")
        result = self.qa_chain.invoke({"query": query})
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"],
            "strategy": "MultiRAG"
        }