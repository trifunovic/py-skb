from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_pinecone import Pinecone

from src.utils.pinecone_utils import get_pinecone_index
from src.services.embedding_service import embedding_service
from src.config import Config


def run_rag_chain(session_id: str, user_input: str):
    config = Config()
    redis_url = f"redis://{config.redis_host}:{config.redis_port}"
    history = RedisChatMessageHistory(session_id=session_id, url=redis_url)
    memory = ConversationBufferMemory(
        chat_memory=history,
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )

    index = get_pinecone_index()
    vectorstore = Pinecone(
        index=index,
        embedding=embedding_service,
        text_key="content",
        namespace=config.pinecone_namespace
    )

    retriever = vectorstore.as_retriever()

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0),
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        output_key="answer"
    )

    result = chain.invoke({"question": user_input})

    return {
        "answer": result["answer"],
        "source_documents": [doc.metadata for doc in result.get("source_documents", [])]
    }
