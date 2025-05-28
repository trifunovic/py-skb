from pinecone import Pinecone, ServerlessSpec
from src.config import Config

config = Config()
pc = Pinecone(api_key=config.pinecone_api_key)

def get_pinecone_index(dimension: int):
    """
    Retrieve or create the Pinecone index using centralized config.
    You must pass the vector dimension explicitly.
    """
    index_name = config.pinecone_index_name
    existing_indexes = [idx['name'] for idx in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=config.pinecone_metric,
            spec=ServerlessSpec(
                cloud=config.pinecone_cloud,
                region=config.pinecone_region
            )
        )

    return pc.Index(index_name)

def upsert_vector(index, vectors):
    return index.upsert(vectors=vectors, namespace=config.pinecone_namespace)

def query_vector(index, vector, top_k=5):
    return index.query(vector=vector, top_k=top_k, namespace=config.pinecone_namespace)

def delete_vector(index, ids):
    return index.delete(ids=ids, namespace=config.pinecone_namespace)

def fetch_vector(index, ids):
    return index.fetch(ids=ids, namespace=config.pinecone_namespace)
