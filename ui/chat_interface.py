import streamlit as st
from typing import List, Dict, Any
from langchain_core.documents import Document
import time

def render_chat():
    """
    Render the chat interface with message history and input.
    """
    # Initialize chat history in session state if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            # If it's an assistant message, show sources and strategy
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📎 Sources"):
                    for i, doc in enumerate(message["sources"]):
                        source = doc.metadata.get("source", "Unknown")
                        page = doc.metadata.get("page_number", "N/A")
                        # Truncate content for display
                        content = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                        st.markdown(f"**Source {i+1}:** {source} (Page: {page})")
                        st.markdown(f"*{content}*")
                        st.divider()
                # Show strategy badge
                strategy = message.get("strategy", "Unknown")
                strategy_class = f"strategy-badge {strategy}"
                st.markdown(
                    f'<span class="{strategy_class}">{strategy}</span>',
                    unsafe_allow_html=True,
                )

    # Chat input
    if prompt := st.chat_input("Ask anything about your documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message immediately
        with st.chat_message("user"):
            st.write(prompt)

        # Check if we have documents indexed
        vector_store = st.session_state.get('vector_store')
        if not vector_store or not vector_store.collection_exists():
            # Show friendly message if no documents
            with st.chat_message("assistant"):
                st.write("Please upload and process documents first to ask questions.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Please upload and process documents first to ask questions.",
                "sources": [],
                "strategy": "None"
            })
            return

        # Get selected strategy from session state (set by sidebar)
        strategy = st.session_state.get('selected_strategy', 'VectorRAG')
        llm = st.session_state.get('llm')
        all_docs = st.session_state.get('all_docs', [])

        if not llm:
            with st.chat_message("assistant"):
                st.error("❌ LLM not initialized. Please ensure GROQ_API_KEY is set in the .env file.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "LLM not initialized. Please ensure GROQ_API_KEY is set in the .env file.",
                "sources": [],
                "strategy": "Error"
            })
            return

        # Show loading indicator
        with st.chat_message("assistant"):
            with st.spinner(f"Thinking with {strategy}..."):
                try:
                    # Get retriever
                    retriever = vector_store.get_retriever(k=st.session_state.get('max_docs', 5))
                    
                    # Import RAG factory
                    from rag.rag_factory import RAGFactory
                    
                    # Create RAG chain
                    rag_chain = RAGFactory.get_chain(
                        strategy=strategy,
                        retriever=retriever,
                        llm=llm,
                        all_docs=all_docs
                    )
                    
                    # Invoke the chain
                    result = rag_chain.invoke(prompt)
                    
                    # Display the answer
                    st.write(result["answer"])
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["source_documents"],
                        "strategy": result["strategy"]
                    })
                    
                except Exception as e:
                    error_msg = str(e)
                    # Provide user-friendly error messages
                    if "model_decommissioned" in error_msg:
                        error_msg = "The selected model has been decommissioned. Please contact support."
                    elif "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                        error_msg = "Authentication failed. Please check your Groq API key in the .env file."
                    elif "rate limit" in error_msg.lower():
                        error_msg = "Rate limit exceeded. Please try again later."
                    
                    st.error(f"❌ Error: {error_msg}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"An error occurred: {error_msg}",
                        "sources": [],
                        "strategy": "Error"
                    })

    # Clear chat button
    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()