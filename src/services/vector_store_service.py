from src.services.embeding_service import EmbeddingService
from src.utils.pinecone_utils import (
    get_pinecone_index,
    upsert_vector,
    query_vector,
    delete_vector,
    fetch_vector
)
from src.config import Config
from src.models.document import Document

config = Config()
embedding_service = EmbeddingService()
_index = None

def _get_index():
    global _index
    if _index is None:
        _index = get_pinecone_index(dimension=embedding_service.dimensions)
    return _index

def add_document(document_id: str, text: str, metadata: dict):
    embedding = embedding_service.embed(text)
    metadata = metadata.copy()
    metadata['content'] = text
    metadata['id'] = document_id

    print("🟡 Payload to Pinecone:")
    print({
        "id": document_id,
        "values": embedding[:5],  # prikaz samo prvih 5 brojeva
        "metadata": metadata
    })

    upsert_vector(_get_index(), [(document_id, embedding, metadata)])

def insert_document(doc: Document):
    embedding = embedding_service.embed(doc.content)
    metadata = doc.metadata.copy()
    metadata['content'] = doc.content
    metadata['id'] = doc.id
    upsert_vector(_get_index(), [(doc.id, embedding, metadata)])
    return {"id": doc.id, "status": "inserted"}

def rebuild_index(documents: list[Document]):
    index = _get_index()
    index.delete(delete_all=True, namespace=config.pinecone_namespace)

    vectors = []
    for doc in documents:
        embedding = embedding_service.embed(doc.content)
        metadata = doc.metadata
        metadata['id'] = doc.id

        print("🟡 Single vector payload:")
        print({
            "id": doc.id,
            "values": embedding[:5],
            "metadata": metadata
        })

        vectors.append((doc.id, embedding, metadata))

    print("🟡 All vectors payload:")
    print(vectors)

    upsert_vector(index, vectors)
    return {"status": "success", "inserted": [{"id": doc.id} for doc in documents]}

def search_similar(text: str, top_k: int = 5):
    query_embedding = embedding_service.embed(text)
    return query_vector(_get_index(), query_embedding, top_k=top_k)

def remove_document(document_id: str):
    delete_vector(_get_index(), [document_id])

def get_document(document_id: str):
    return fetch_vector(_get_index(), [document_id])

def remove_all_documents():
    index = _get_index()
    delete_vector(index, ids=[])
    index.delete(delete_all=True, namespace=config.pinecone_namespace)

def list_all_document_ids() -> list[str]:
    raise NotImplementedError("Pinecone ne podržava direktno listanje svih ID-jeva — koristi eksterni storage.")

def get_all_documents(known_ids: list[str]) -> list[Document]:
    index = _get_index()
    print(f"DEBUG: fetch_vector = {fetch_vector}")
    print(f"DEBUG: index = {index}")
    print(f"DEBUG: known_ids = {known_ids}")
    response = fetch_vector(index, known_ids)

    documents: list[Document] = []
    for doc_id, data in response.items():
        metadata = data.get('metadata', {})
        content = metadata.get('content', '')
        documents.append(Document(id=doc_id, content=content, metadata=metadata))

    return documents
