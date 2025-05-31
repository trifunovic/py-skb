from langchain_community.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.config import Config
from src.utils.pinecone_utils import get_pinecone_index
from src.services.embedding_service import EmbeddingService
import traceback
from typing import Optional

config = Config()
embedding_service = EmbeddingService()

# Use centralized embedding model
embedding_model = embedding_service.model
embedding = HuggingFaceEmbeddings(model_name=config.model_name)

# Load Pinecone index
index = get_pinecone_index()
vectorstore = Pinecone(index, embedding, text_key="content", namespace=config.pinecone_namespace)

# LLM instance
llm = ChatOpenAI(model_name=config.openai_model, api_key=config.openai_api_key)

def run_rag_chain(query: str, top_k: int) -> dict:
    try:
        print(f"🔍 Received query: {query}", flush=True)

        retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

        result = qa_chain.invoke({"query": query})
        docs = retriever.get_relevant_documents(query)

        return {
            "query": query,
            "result": result,
            "retrieved_docs": [
                {"id": d.metadata.get("id", "n/a"), "content": d.page_content, "metadata": d.metadata}
                for d in docs
            ]
        }
    except Exception as e:
        print("❌ RAG chain execution failed:", flush=True)
        traceback.print_exc()
        raise RuntimeError(f"RAG chain failed: {e}")
