from langchain_community.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from src.config import Config
from src.utils.pinecone_utils import get_pinecone_index
from src.services.embedding_service import EmbeddingService
import traceback
from langchain_community.embeddings import HuggingFaceEmbeddings

config = Config()
embedding_service = EmbeddingService()

# Use centralized embedding model (OpenAI or local)
embedding_model = embedding_service.model

# Load Pinecone index
index = get_pinecone_index()

# Create vector store
embedding = HuggingFaceEmbeddings(model_name=config.model_name)
vectorstore = Pinecone(index, embedding, text_key="content", namespace=config.pinecone_namespace)

# Setup retrieval chain
llm = ChatOpenAI(model_name=config.openai_model, api_key=config.openai_api_key)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

def run_rag_chain(query: str) -> str:
    try:
        print(f"🔍 Received query: {query}", flush=True)
        result = qa_chain.invoke({"query": query})
        print(f"✅ Chain result: {result}", flush=True)
        return result
    except Exception as e:
        print("❌ RAG chain execution failed:", flush=True)
        traceback.print_exc()
        raise RuntimeError(f"RAG chain failed: {e}")
