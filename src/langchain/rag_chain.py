from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from pinecone import Pinecone
from src.config import Config

config = Config()

# Novi način inicijalizacije Pinecone klijenta
pc = Pinecone(api_key=config.pinecone_api_key, environment=config.pinecone_region)
index = pc.Index(config.pinecone_index_name)

embedding = OpenAIEmbeddings()

vectorstore = LangchainPinecone(
    index=index,
    embedding=embedding,
    text_key="content",
    namespace=config.pinecone_namespace,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": config.search_top_k})

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    retriever=retriever
)

def run_qa(query: str) -> str:
    return qa_chain.run(query)
