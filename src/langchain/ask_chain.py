from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_pinecone import Pinecone

from src.utils.pinecone_utils import get_pinecone_index
from src.services.embedding_service import embedding_service
from src.config import Config


def run_ask_chain(question: str, top_k: int = 4):
    config = Config()

    index = get_pinecone_index()
    vectorstore = Pinecone(
        index=index,
        embedding=embedding_service,
        text_key="content",
        namespace=config.pinecone_namespace
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    result = chain({"query": question})

    return {
        "query": question,
        "result": result,
        "retrieved_docs": [doc.metadata for doc in result.get("source_documents", [])]
    }
