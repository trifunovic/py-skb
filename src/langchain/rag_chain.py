from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
import pinecone
import os

from src.config import Config

# Učitaj konfiguraciju
config = Config()

# Inicijalizuj Pinecone
pinecone.init(api_key=config.pinecone_api_key, environment=config.pinecone_region)
index = pinecone.Index(config.pinecone_index_name)

# Embedding model
embedding_model = OpenAIEmbeddings()

# Kreiraj LangChain retriever iz Pinecone indeksa
retriever = Pinecone(
    index,  # Pinecone index objekat
    embedding_model.embed_query,  # funkcija za kreiranje vektora iz query teksta
    "content"  # polje koje sadrži glavni tekst u documentima
).as_retriever(search_kwargs={"k": config.search_top_k})

# Inicijalizuj LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Kreiraj QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

# Ekspozuj funkciju
def run_qa(question: str) -> str:
    return qa_chain.run(question)
