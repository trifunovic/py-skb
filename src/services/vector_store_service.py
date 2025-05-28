from src.services.embeding_service import EmbeddingService
from src.utils.pinecone_utils import (
    get_pinecone_index,
    upsert_vector,
    query_vector,
    delete_vector,
    fetch_vector
)
from src.config import Config

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
    upsert_vector(_get_index(), [(document_id, embedding, metadata)])

def search_similar(text: str, top_k: int = 5):
    query_embedding = embedding_service.embed(text)
    return query_vector(_get_index(), query_embedding, top_k=top_k)

def remove_document(document_id: str):
    delete_vector(_get_index(), [document_id])

def get_document(document_id: str):
    return fetch_vector(_get_index(), [document_id])

def remove_all_documents():
    index = _get_index()
    delete_vector(index, ids=[])  # optional cleanup call
    index.delete(delete_all=True, namespace=config.pinecone_namespace)

def list_all_document_ids() -> list[str]:
    index = _get_index()
    response = index.describe_index_stats(namespace=config.pinecone_namespace)
    return list(response.get("namespaces", {}).get(config.pinecone_namespace, {}).get("vector_count", 0))

def list_all_document_ids() -> list[str]:
    index = _get_index()
    stats = index.describe_index_stats(namespace=config.pinecone_namespace)
    ns_info = stats.get("namespaces", {}).get(config.pinecone_namespace, {})
    if not ns_info:
        return []
    # Pinecone ne vraća direktno ID-jeve → moraš da ih upišeš ili čuvaš odvojeno
    raise NotImplementedError("Pinecone ne podržava listanje svih ID-jeva bez eksternog čuvanja.")


