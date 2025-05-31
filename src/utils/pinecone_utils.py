from pinecone import Pinecone, ServerlessSpec
from src.config import Config
from src.services.embedding_service import EmbeddingService

config = Config()
embedding_service = EmbeddingService()
pc = Pinecone(api_key=config.pinecone_api_key)

def get_pinecone_index():
    """
    Retrieve or create the Pinecone index using config and embedding model's dimensions.
    """
    index_name = config.pinecone_index_name
    dimension = embedding_service.dimensions
    existing_indexes = [idx['name'] for idx in pc.list_indexes()]

    if index_name not in existing_indexes:
        print(f"Creating index '{index_name}' with dimension {dimension}...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=config.pinecone_metric,
            spec=ServerlessSpec(
                cloud=config.pinecone_cloud,
                region=config.pinecone_region
            )
        )
    else:
        print(f"Pinecone index '{index_name}' already exists.")

    return pc.Index(index_name)

def upsert_vector(index, vectors):
    return index.upsert(vectors=vectors, namespace=config.pinecone_namespace)

def query_vector(index, vector, top_k=5):
    return index.query(vector=vector, top_k=top_k, namespace=config.pinecone_namespace)

def delete_vector(index, ids):
    return index.delete(ids=ids, namespace=config.pinecone_namespace)

def fetch_vector(index, ids):
    return index.fetch(ids=ids, namespace=config.pinecone_namespace)
