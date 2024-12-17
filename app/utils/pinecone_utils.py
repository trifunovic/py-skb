from pinecone import Pinecone, ServerlessSpec
from config import config
from services.embeding_service import EmbeddingService

# Initialize Pinecone client
pc = Pinecone(api_key=config.pinecone_api_key)

# Initialize EmbeddingService
embedding_service = EmbeddingService()

def get_pinecone_index():
    """
    Retrieve or create the Pinecone index using centralized config.
    """
    index_name = config.pinecone_index_name

    # Ensure the index exists
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=embedding_service.dimensions,  # Dynamically set dimension
            metric=config.pinecone_metric,
            spec=ServerlessSpec(
                cloud=config.pinecone_cloud,
                region=config.pinecone_region
            )
        )
    # Retrieve the index
    return pc.Index(index_name)  # Use the Index method
