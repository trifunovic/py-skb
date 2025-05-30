from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document

from src.services.vector_store_service import query_vector
from src.services.embeding_service import EmbeddingService

class CustomRetriever:
    def __init__(self, embedding_service: EmbeddingService, top_k: int = 3):
        self.embedding_service = embedding_service
        self.top_k = top_k

    def get_relevant_documents(self, query: str) -> list[Document]:
        embedding = self.embedding_service.embed(query)
        results = query_vector(vector=embedding, top_k=self.top_k)
        return [
            Document(page_content=item["content"], metadata=item.get("metadata", {}))
            for item in results
        ]

embedding_service = EmbeddingService()
retriever = CustomRetriever(embedding_service=embedding_service)

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4", temperature=0),
    chain_type="stuff",
    retriever=retriever
)

def run_qa(question: str) -> str:
    return qa_chain.run(question)
